import time
from typing import Dict, Optional, Any
from contextlib import asynccontextmanager, contextmanager

class TimingCollector:
    def __init__(self):
        self.timings: Dict[str, float] = {}

    def record(self, stage: str, duration_ms: float):
        self.timings[stage] = round(duration_ms, 2)

    def get(self, stage: str, default: float = 0.0) -> float:
        return self.timings.get(stage, default)

    @contextmanager
    def time_sync(self, stage: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            self.record(stage, elapsed_ms)

    @asynccontextmanager
    async def time_async(self, stage: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            self.record(stage, elapsed_ms)

    def to_dict(self) -> Dict[str, float]:
        return dict(self.timings)
