import re
from typing import List, Dict, Any, Optional
from .base import BaseChunker
from ..models.schemas import Chunk, ChunkMetadata

class FixedSizeChunker(BaseChunker):
    """
    Strategy 1: Fixed-size chunking with sliding window overlap.
    Splits text into chunks of `chunk_size` words/tokens with `overlap` tokens.
    """
    def __init__(self, chunk_size: int = 120, overlap: int = 25):
        super().__init__(name="fixed_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        meta = metadata or {}
        # Clean and split into words
        words = text.split()
        if not words:
            return []

        chunks: List[Chunk] = []
        step = max(1, self.chunk_size - self.overlap)
        
        chunk_idx = 0
        for i in range(0, len(words), step):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk_id = f"{doc_id}_fixed_{chunk_idx}"
            chunk_meta = ChunkMetadata(
                doc_id=doc_id,
                passage_idx=meta.get("passage_idx", 0),
                lang=meta.get("lang", "en"),
                query_type=meta.get("query_type"),
                is_selected=meta.get("is_selected", 0),
                strategy="fixed_size",
                start_char=0,
                end_char=len(chunk_text),
                token_count=len(chunk_words),
                extra={"window_start": i, "window_end": i + len(chunk_words)}
            )
            
            chunks.append(Chunk(
                id=chunk_id,
                text=chunk_text,
                score=0.0,
                metadata=chunk_meta
            ))
            chunk_idx += 1
            
            if i + self.chunk_size >= len(words):
                break

        return chunks
