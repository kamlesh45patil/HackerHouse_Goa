import numpy as np
from fastapi import APIRouter, Query
from typing import Dict, Any
from ..models.schemas import BenchmarkReport, BenchmarkMetric
from ..pipeline.orchestrator import RAGOrchestrator
from ..indexing.dataset_loader import load_msmarco_xi_dataset
from ..indexing.eval_chunking import evaluate_chunking_strategies

router = APIRouter(prefix="/api", tags=["Evaluation & Benchmarking"])
orchestrator = RAGOrchestrator()

def compute_metric(values: list) -> BenchmarkMetric:
    if not values:
        return BenchmarkMetric(p50=0, p70=0, p90=0, p99=0, p100=0, mean=0, min=0, max=0, count=0)
    arr = np.array(values)
    return BenchmarkMetric(
        p50=round(float(np.percentile(arr, 50)), 2),
        p70=round(float(np.percentile(arr, 70)), 2),
        p90=round(float(np.percentile(arr, 90)), 2),
        p99=round(float(np.percentile(arr, 99)), 2),
        p100=round(float(np.percentile(arr, 100)), 2),
        mean=round(float(np.mean(arr)), 2),
        min=round(float(np.min(arr)), 2),
        max=round(float(np.max(arr)), 2),
        count=len(values)
    )

@router.get("/benchmark/run", response_model=BenchmarkReport)
async def run_benchmark_endpoint(num_queries: int = Query(20, ge=5, le=100)):
    records = load_msmarco_xi_dataset()
    queries = []
    for r in records:
        if r.get("query"):
            queries.append(r.get("query"))
        if r.get("Eng_Query"):
            queries.append(r.get("Eng_Query"))
    
    selected_queries = (queries * (num_queries // len(queries) + 1))[:num_queries]

    retrieval_times = []
    generation_times = []
    guardrail_times = []
    core_times = []
    total_times = []

    for q in selected_queries:
        resp = await orchestrator.process_query(query_text=q, top_k=5)
        retrieval_times.append(resp.latencies.retrieval_ms)
        generation_times.append(resp.latencies.generation_ms)
        guardrail_times.append(resp.latencies.guardrail_ms)
        core_times.append(resp.latencies.core_pipeline_ms)
        total_times.append(resp.latencies.total_ms)

    return BenchmarkReport(
        num_queries=len(selected_queries),
        retrieval=compute_metric(retrieval_times),
        generation=compute_metric(generation_times),
        guardrail=compute_metric(guardrail_times),
        core_pipeline=compute_metric(core_times),
        total=compute_metric(total_times)
    )

@router.get("/chunking/comparison")
async def get_chunking_comparison():
    return evaluate_chunking_strategies()
