import re
import numpy as np
from typing import List, Dict, Any, Optional
from .base import BaseChunker
from ..models.schemas import Chunk, ChunkMetadata

class SemanticChunker(BaseChunker):
    """
    Strategy 2: Semantic Chunking.
    Splits text into sentences (handles English and Indic sentence terminators like ।, .),
    calculates semantic similarity between adjacent sentences, and cuts chunks
    at semantic discontinuities (valleys in cosine similarity).
    """
    def __init__(self, threshold_percentile: float = 40.0, min_chunk_words: int = 30, max_chunk_words: int = 150):
        super().__init__(name="semantic")
        self.threshold_percentile = threshold_percentile
        self.min_chunk_words = min_chunk_words
        self.max_chunk_words = max_chunk_words

    def _split_into_sentences(self, text: str) -> List[str]:
        # Support Latin terminators (.!?) and Indic Purna Viram (।)
        pattern = r'(?<=[.!?।\n])\s+'
        sentences = [s.strip() for s in re.split(pattern, text) if s.strip()]
        return sentences if sentences else [text]

    def _compute_fallback_similarity(self, s1: str, s2: str) -> float:
        """Lightweight Jaccard + token overlap similarity if embedding model is not called per-split."""
        words1 = set(re.findall(r'\w+', s1.lower()))
        words2 = set(re.findall(r'\w+', s2.lower()))
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union if union > 0 else 0.0

    def chunk_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        meta = metadata or {}
        sentences = self._split_into_sentences(text)
        
        if len(sentences) <= 1:
            chunk_meta = ChunkMetadata(
                doc_id=doc_id,
                passage_idx=meta.get("passage_idx", 0),
                lang=meta.get("lang", "en"),
                query_type=meta.get("query_type"),
                is_selected=meta.get("is_selected", 0),
                strategy="semantic",
                start_char=0,
                end_char=len(text),
                token_count=len(text.split())
            )
            return [Chunk(id=f"{doc_id}_sem_0", text=text, metadata=chunk_meta)]

        # Calculate distances between adjacent sentences
        similarities = []
        for i in range(len(sentences) - 1):
            sim = self._compute_fallback_similarity(sentences[i], sentences[i + 1])
            similarities.append(sim)

        threshold = float(np.percentile(similarities, self.threshold_percentile)) if similarities else 0.0

        chunks: List[Chunk] = []
        current_sentences: List[str] = [sentences[0]]
        current_words = len(sentences[0].split())
        chunk_idx = 0

        for i in range(1, len(sentences)):
            sim = similarities[i - 1]
            sent = sentences[i]
            sent_words = len(sent.split())

            # Split condition: similarity drops below threshold AND minimum chunk size met, OR exceeds max words
            is_discontinuity = (sim <= threshold and current_words >= self.min_chunk_words)
            is_oversized = (current_words + sent_words > self.max_chunk_words and current_words >= self.min_chunk_words)

            if is_discontinuity or is_oversized:
                chunk_text = " ".join(current_sentences)
                chunk_id = f"{doc_id}_sem_{chunk_idx}"
                chunk_meta = ChunkMetadata(
                    doc_id=doc_id,
                    passage_idx=meta.get("passage_idx", 0),
                    lang=meta.get("lang", "en"),
                    query_type=meta.get("query_type"),
                    is_selected=meta.get("is_selected", 0),
                    strategy="semantic",
                    start_char=0,
                    end_char=len(chunk_text),
                    token_count=len(chunk_text.split()),
                    extra={"sentence_count": len(current_sentences), "split_sim": sim}
                )
                chunks.append(Chunk(id=chunk_id, text=chunk_text, metadata=chunk_meta))
                chunk_idx += 1
                current_sentences = [sent]
                current_words = sent_words
            else:
                current_sentences.append(sent)
                current_words += sent_words

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunk_id = f"{doc_id}_sem_{chunk_idx}"
            chunk_meta = ChunkMetadata(
                doc_id=doc_id,
                passage_idx=meta.get("passage_idx", 0),
                lang=meta.get("lang", "en"),
                query_type=meta.get("query_type"),
                is_selected=meta.get("is_selected", 0),
                strategy="semantic",
                start_char=0,
                end_char=len(chunk_text),
                token_count=len(chunk_text.split()),
                extra={"sentence_count": len(current_sentences)}
            )
            chunks.append(Chunk(id=chunk_id, text=chunk_text, metadata=chunk_meta))

        return chunks
