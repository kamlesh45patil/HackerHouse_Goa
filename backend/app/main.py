import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

from .api.transcribe import router as transcribe_router
from .api.query import router as query_router, orchestrator
from .api.benchmark import router as benchmark_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Voice RAG Orchestrator and FAISS index...")
    orchestrator.initialize()
    yield
    print("Shutting down Voice RAG service.")

app = FastAPI(
    title="Voice-Enabled RAG System API",
    description="Multilingual Indic Voice RAG with FAISS, Sarvam STT, and Gemini Flash (<200ms target)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router)
app.include_router(query_router)
app.include_router(benchmark_router)

@app.get("/")
async def root():
    return {
        "service": "Voice-Enabled RAG System API",
        "event": "Hacker House Goa 2026",
        "status": "healthy",
        "frontend_demo": "http://localhost:3000",
        "interactive_swagger_docs": "http://localhost:8000/docs",
        "endpoints": {
            "query": "POST /api/query",
            "transcribe": "POST /api/transcribe",
            "benchmark": "GET /api/benchmark/run",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Voice-Enabled RAG System",
        "event": "Hacker House Goa 2026",
        "version": "1.0.0"
    }
