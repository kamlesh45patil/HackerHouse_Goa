from fastapi import APIRouter, UploadFile, File, Form, Body, Request
from typing import Optional
from ..models.schemas import PipelineResponse, PipelineQueryRequest
from ..pipeline.orchestrator import RAGOrchestrator

router = APIRouter(prefix="/api", tags=["RAG Pipeline"])
orchestrator = RAGOrchestrator()

@router.post("/query", response_model=PipelineResponse)
async def query_pipeline_endpoint(
    request: Request,
    query: Optional[str] = Form(None),
    language: Optional[str] = Form("auto"),
    top_k: int = Form(5),
    audio: Optional[UploadFile] = File(None)
):
    audio_bytes = None
    if audio is not None:
        audio_bytes = await audio.read()

    # If JSON body was passed instead of Form data
    if not query and not audio_bytes:
        try:
            body = await request.json()
            query = body.get("query")
            language = body.get("language", "auto")
            top_k = body.get("top_k", 5)
        except Exception:
            pass

    response = await orchestrator.process_query(
        query_text=query,
        audio_bytes=audio_bytes,
        language=language or "auto",
        top_k=top_k
    )
    return response
