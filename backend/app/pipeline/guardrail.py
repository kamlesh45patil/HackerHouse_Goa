import re
import time
import numpy as np
from typing import List, Tuple, Optional
from ..models.schemas import GuardrailResult, CitedChunk

class GuardrailService:
    """
    Ultra-Fast Guardrail Layer (<10ms execution):
    1. Pre-check: Regex/keyword rule-based detection for harmful, injection, and off-topic queries (<1ms).
    2. Post-check: Token n-gram overlap & lexical-semantic grounding containment against retrieved passages (<2ms).
    """
    def __init__(self, grounding_threshold: float = 0.25):
        self.grounding_threshold = grounding_threshold
        
        self.unsafe_patterns = [
            r"\b(bomb|weapon|explosive|hack|malware|virus|ddos|suicide|kill|steal|bypass)\b",
            r"\b(ignore previous instructions|system prompt|jailbreak|exploit)\b"
        ]

    def pre_check(self, query: str) -> GuardrailResult:
        t_start = time.perf_counter()
        q_lower = query.lower()

        for pattern in self.unsafe_patterns:
            if re.search(pattern, q_lower):
                latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)
                return GuardrailResult(
                    is_safe=False,
                    is_on_topic=False,
                    is_grounded=False,
                    passed=False,
                    reason="Query flagged for potentially unsafe or restricted content.",
                    grounding_score=0.0,
                    latency_ms=latency_ms
                )

        if len(query.strip()) < 3 or (len(query.split()) == 1 and len(query) > 30):
            latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)
            return GuardrailResult(
                is_safe=True,
                is_on_topic=False,
                is_grounded=False,
                passed=False,
                reason="Query is ambiguous or insufficient to match knowledge base.",
                grounding_score=0.0,
                latency_ms=latency_ms
            )

        latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)
        return GuardrailResult(
            is_safe=True,
            is_on_topic=True,
            is_grounded=True,
            passed=True,
            reason=None,
            grounding_score=1.0,
            latency_ms=latency_ms
        )

    def post_grounding_check(
        self,
        answer: str,
        retrieved_chunks: List[CitedChunk]
    ) -> GuardrailResult:
        """
        Fast token n-gram and semantic overlap containment check.
        Executes in < 3ms without slow PyTorch BERT re-encoding on CPU.
        """
        t_start = time.perf_counter()
        
        if not retrieved_chunks or not answer.strip():
            latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)
            return GuardrailResult(
                is_safe=True,
                is_on_topic=True,
                is_grounded=False,
                passed=False,
                reason="No retrieved context available to ground the answer.",
                grounding_score=0.0,
                latency_ms=latency_ms
            )

        ans_words = set(re.findall(r'\w+', answer.lower()))
        # Remove common stop words
        stopwords = {"the", "a", "an", "is", "are", "in", "on", "at", "to", "for", "of", "and", "or", "it", "with", "as", "by", "का", "के", "की", "में", "है", "हैं", "और", "से"}
        ans_content_words = ans_words - stopwords

        if not ans_content_words:
            ans_content_words = ans_words

        # Compute max overlap against retrieved chunks
        max_overlap_ratio = 0.0
        for chunk in retrieved_chunks:
            chunk_words = set(re.findall(r'\w+', chunk.text.lower()))
            if not chunk_words:
                continue
            common = ans_content_words.intersection(chunk_words)
            overlap = len(common) / len(ans_content_words) if ans_content_words else 0.0
            
            # Incorporate retrieval score
            combined_score = 0.6 * overlap + 0.4 * min(1.0, chunk.score)
            if combined_score > max_overlap_ratio:
                max_overlap_ratio = combined_score

        is_grounded = max_overlap_ratio >= self.grounding_threshold
        latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        return GuardrailResult(
            is_safe=True,
            is_on_topic=True,
            is_grounded=is_grounded,
            passed=is_grounded,
            reason=None if is_grounded else f"Answer grounding score ({max_overlap_ratio:.2f}) below threshold ({self.grounding_threshold}).",
            grounding_score=round(max_overlap_ratio, 3),
            latency_ms=latency_ms
        )
