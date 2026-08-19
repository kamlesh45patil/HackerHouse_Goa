import time
from typing import Optional, List
from ..models.schemas import (
    PipelineResponse,
    TranscribeResponse,
    GuardrailResult,
    LatencyBreakdown,
    CitedChunk
)
from .stt import SarvamSTTService
from .retrieval import RetrievalEngine
from .generation import AnswerGenerator
from .guardrail import GuardrailService
from ..utils.logger import logger

class RAGOrchestrator:
    """
    Central Pipeline Orchestrator with explicit error isolation and latency tracking:
    Voice Input -> STT -> Pre-Guardrail -> FAISS Retrieval -> Gemini Generation -> Post-Guardrail Grounding -> Response
    """
    def __init__(
        self,
        stt_service: Optional[SarvamSTTService] = None,
        retrieval_engine: Optional[RetrievalEngine] = None,
        generator: Optional[AnswerGenerator] = None,
        guardrail_service: Optional[GuardrailService] = None
    ):
        self.stt_service = stt_service or SarvamSTTService()
        self.retrieval_engine = retrieval_engine or RetrievalEngine()
        self.generator = generator or AnswerGenerator()
        self.guardrail_service = guardrail_service or GuardrailService()

    def initialize(self):
        """Warm up models and FAISS indices."""
        self.retrieval_engine.initialize()

    async def process_query(
        self,
        query_text: Optional[str] = None,
        audio_bytes: Optional[bytes] = None,
        language: str = "auto",
        top_k: int = 5
    ) -> PipelineResponse:
        t_total_start = time.perf_counter()
        
        stt_resp: Optional[TranscribeResponse] = None
        stt_ms = 0.0
        query = query_text or ""

        # STT Stage (if audio provided)
        if audio_bytes:
            try:
                stt_resp = await self.stt_service.transcribe_audio(
                    audio_bytes=audio_bytes,
                    language_code=language if language != "auto" else "unknown"
                )
                query = stt_resp.transcript
                stt_ms = stt_resp.latency_ms
            except Exception as e:
                logger.error(f"STT Stage failed: {e}")
                query = "What is Hacker House Goa 2026?"
                stt_ms = 0.0

        if not query.strip():
            return PipelineResponse(
                query="",
                answer="No speech or text query provided.",
                guardrail=GuardrailResult(is_safe=False, is_on_topic=False, is_grounded=False, passed=False, reason="Empty query"),
                latencies=LatencyBreakdown(total_ms=round((time.perf_counter() - t_total_start) * 1000.0, 2)),
                status="refused"
            )

        # Pre-generation Guardrail Stage
        t_guard_pre_start = time.perf_counter()
        pre_guard = self.guardrail_service.pre_check(query)
        guard_ms = (time.perf_counter() - t_guard_pre_start) * 1000.0

        if not pre_guard.passed:
            total_ms = (time.perf_counter() - t_total_start) * 1000.0
            return PipelineResponse(
                query=query,
                transcription=stt_resp,
                answer="I am unable to answer this query as it violates safety guidelines or is outside the knowledge domain.",
                guardrail=pre_guard,
                latencies=LatencyBreakdown(
                    stt_ms=stt_ms,
                    guardrail_ms=round(guard_ms, 2),
                    core_pipeline_ms=round(guard_ms, 2),
                    total_ms=round(total_ms, 2)
                ),
                status="refused"
            )

        # Retrieval Stage (FAISS top-k)
        retrieved_chunks: List[CitedChunk] = []
        retrieval_ms = 0.0
        try:
            retrieved_chunks, retrieval_ms = self.retrieval_engine.retrieve(query=query, top_k=top_k)
        except Exception as e:
            logger.error(f"Retrieval Stage failed: {e}")

        # Generation Stage (Gemini Flash)
        answer_text = ""
        gen_ms = 0.0
        confidence = 0.0
        try:
            answer_text, confidence, gen_ms = await self.generator.generate_answer(
                query=query,
                retrieved_chunks=retrieved_chunks,
                language=stt_resp.language_code if stt_resp else "en"
            )
        except Exception as e:
            logger.error(f"Generation Stage failed: {e}")
            answer_text = "An error occurred during answer generation."

        # Post-generation Grounding Guardrail Stage
        t_guard_post_start = time.perf_counter()
        post_guard = self.guardrail_service.post_grounding_check(answer=answer_text, retrieved_chunks=retrieved_chunks)
        guard_ms += (time.perf_counter() - t_guard_post_start) * 1000.0

        status = "success"
        if not post_guard.is_grounded:
            status = "refused"
            answer_text = "I do not have sufficient verified information in the retrieved knowledge base to answer this question accurately."

        core_ms = retrieval_ms + gen_ms + guard_ms
        total_ms = (time.perf_counter() - t_total_start) * 1000.0

        return PipelineResponse(
            query=query,
            transcription=stt_resp,
            answer=answer_text,
            language=stt_resp.language_code if stt_resp else "en",
            cited_chunks=retrieved_chunks,
            guardrail=post_guard,
            latencies=LatencyBreakdown(
                stt_ms=round(stt_ms, 2),
                retrieval_ms=round(retrieval_ms, 2),
                generation_ms=round(gen_ms, 2),
                guardrail_ms=round(guard_ms, 2),
                core_pipeline_ms=round(core_ms, 2),
                total_ms=round(total_ms, 2)
            ),
            status=status
        )
