import os
import json
import time
import numpy as np
from typing import List, Optional, Tuple, Dict, Any
from ..models.schemas import Chunk, ChunkMetadata, CitedChunk
from ..indexing.build_index import get_embedding_model, build_faiss_index
from ..utils.faiss_adapter import faiss

class RetrievalEngine:
    """
    High-speed FAISS vector retrieval engine targeting <50ms lookup.
    Loads in-memory FAISS IndexFlatIP with L2-normalized 768-dim embeddings.
    """
    def __init__(self, data_dir: str = "backend/data", index_name: str = "faiss_index.bin", chunks_name: str = "chunks.json"):
        self.data_dir = data_dir
        self.index_path = os.path.join(data_dir, index_name)
        self.chunks_path = os.path.join(data_dir, chunks_name)
        self.index = None
        self.chunks: List[Chunk] = []
        self.model = None

    def initialize(self):
        self.model = get_embedding_model()
        
        if not os.path.exists(self.index_path) or not os.path.exists(self.chunks_path):
            self.index, chunks_dicts = build_faiss_index(strategy_name="metadata_aware", data_dir=self.data_dir)
            self.chunks = [Chunk(**c) for c in chunks_dicts]
        else:
            self.index = faiss.read_index(self.index_path)
            with open(self.chunks_path, "r", encoding="utf-8") as f:
                chunks_dicts = json.load(f)
                self.chunks = [Chunk(**c) for c in chunks_dicts]

    def retrieve(self, query: str, top_k: int = 5, min_score: float = 0.35) -> Tuple[List[CitedChunk], float]:
        if self.index is None or not self.chunks:
            self.initialize()

        t_start = time.perf_counter()

        q_emb = self.model.encode([query])
        q_emb = np.array(q_emb, dtype=np.float32)
        q_norm = np.linalg.norm(q_emb, axis=1, keepdims=True)
        q_norm[q_norm == 0] = 1.0
        q_emb = q_emb / q_norm

        scores, indices = self.index.search(q_emb, min(top_k, len(self.chunks)))
        latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        results: List[CitedChunk] = []
        for rank_idx, chunk_idx in enumerate(indices[0]):
            if 0 <= chunk_idx < len(self.chunks):
                score = float(scores[0][rank_idx])
                # Only include results above minimum relevance threshold
                if score < min_score:
                    continue
                chunk = self.chunks[chunk_idx]
                results.append(CitedChunk(
                    id=chunk.id,
                    text=chunk.text,
                    score=round(score, 4),
                    doc_id=chunk.metadata.doc_id,
                    lang=chunk.metadata.lang,
                    strategy=chunk.metadata.strategy
                ))

        return results, latency_ms
