from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

class ChunkMetadata(BaseModel):
    doc_id: str
    passage_idx: int = 0
    lang: str = "en"
    query_type: Optional[str] = None
    is_selected: int = 0
    strategy: str = "fixed"
    start_char: int = 0
    end_char: int = 0
    token_count: int = 0
    extra: Dict[str, Any] = Field(default_factory=dict)

class Chunk(BaseModel):
    id: str
    text: str
    score: float = 0.0
    metadata: ChunkMetadata

class TranscribeResponse(BaseModel):
    transcript: str
    language_code: str = "hi-IN"
    confidence: float = 1.0
    latency_ms: float = 0.0

class GuardrailResult(BaseModel):
    is_safe: bool = True
    is_on_topic: bool = True
    is_grounded: bool = True
    passed: bool = True
    reason: Optional[str] = None
    grounding_score: float = 1.0
    latency_ms: float = 0.0

class LatencyBreakdown(BaseModel):
    stt_ms: float = 0.0
    retrieval_ms: float = 0.0
    generation_ms: float = 0.0
    guardrail_ms: float = 0.0
    core_pipeline_ms: float = 0.0
    total_ms: float = 0.0

class PipelineQueryRequest(BaseModel):
    query: Optional[str] = None
    language: Optional[str] = "auto"
    top_k: int = 5
    strategy: Optional[str] = None

class CitedChunk(BaseModel):
    id: str
    text: str
    score: float
    doc_id: str
    lang: str
    strategy: str

class PipelineResponse(BaseModel):
    query: str
    transcription: Optional[TranscribeResponse] = None
    answer: str
    language: str = "en"
    cited_chunks: List[CitedChunk] = Field(default_factory=list)
    guardrail: GuardrailResult
    latencies: LatencyBreakdown
    status: str = "success" # success | refused | error
    error_message: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)

class BenchmarkMetric(BaseModel):
    p50: float
    p70: float
    p90: float
    p99: float
    p100: float
    mean: float
    min: float
    max: float
    count: int

class BenchmarkReport(BaseModel):
    num_queries: int
    retrieval: BenchmarkMetric
    generation: BenchmarkMetric
    guardrail: BenchmarkMetric
    core_pipeline: BenchmarkMetric
    total: BenchmarkMetric
    timestamp: float = Field(default_factory=time.time)
