from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..models.schemas import TranscribeResponse
from ..pipeline.stt import SarvamSTTService

router = APIRouter(prefix="/api", tags=["Speech-to-Text"])
stt_service = SarvamSTTService()

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio_endpoint(
    file: UploadFile = File(...),
    language_code: str = Form("unknown")
):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty audio file provided.")
        
        result = await stt_service.transcribe_audio(
            audio_bytes=content,
            filename=file.filename or "audio.wav",
            language_code=language_code
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
