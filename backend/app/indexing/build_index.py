import os
import json
import numpy as np
from typing import List, Tuple, Dict, Any
from ..chunking import get_chunker
from ..models.schemas import Chunk
from .dataset_loader import load_msmarco_xi_dataset
from ..utils.faiss_adapter import faiss

_EMBEDDING_MODEL = None

class FallbackVectorizer:
    """Deterministic dense vectorizer for 768-dim embeddings with L2 normalization."""
    def __init__(self, dim: int = 768):
        self.dim = dim

    def encode(self, texts: List[str], normalize_embeddings: bool = True) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        
        vectors = []
        for text in texts:
            vec = np.zeros(self.dim, dtype=np.float32)
            words = text.lower().split()
            for i, word in enumerate(words):
                h = abs(hash(word))
                idx1 = h % self.dim
                idx2 = (h // self.dim) % self.dim
                sign = 1.0 if (h % 2 == 0) else -1.0
                vec[idx1] += sign * (1.0 / (i + 1)**0.2)
                vec[idx2] += 0.5 * sign
            
            for i in range(len(text) - 2):
                ngram = text[i : i + 3].lower()
                h_ng = abs(hash(ngram)) % self.dim
                vec[h_ng] += 0.25

            norm = np.linalg.norm(vec)
            if norm > 0 and normalize_embeddings:
                vec = vec / norm
            vectors.append(vec)
            
        return np.array(vectors, dtype=np.float32)

def get_embedding_model():
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBEDDING_MODEL = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        except Exception:
            _EMBEDDING_MODEL = FallbackVectorizer(dim=768)
    return _EMBEDDING_MODEL

def build_faiss_index(
    strategy_name: str = "metadata_aware",
    data_dir: str = "backend/data",
    output_index_name: str = "faiss_index.bin",
    output_chunks_name: str = "chunks.json"
) -> Tuple[Any, List[Dict[str, Any]]]:
    os.makedirs(data_dir, exist_ok=True)
    records = load_msmarco_xi_dataset()
    chunker = get_chunker(strategy_name)

    all_chunks: List[Chunk] = []
    
    for r_idx, record in enumerate(records):
        doc_id = str(record.get("query_id", f"doc_{r_idx}"))
        query_type = record.get("query_type", "general")
        passages = record.get("passages", [])

        for p_idx, p in enumerate(passages):
            # Support both flat dict format (normalized) and legacy format
            p_text = p.get("passage_text", "") if isinstance(p, dict) else ""
            if not p_text.strip():
                continue

            meta = {
                "passage_idx": p_idx,
                "lang": p.get("lang", record.get("target_lang", "en")),
                "query_type": query_type,
                "is_selected": p.get("is_selected", 0),
                "url": p.get("url", "")
            }

            chunks = chunker.chunk_document(doc_id=doc_id, text=p_text, metadata=meta)
            all_chunks.extend(chunks)

    # Generate embeddings
    model = get_embedding_model()
    texts = [c.text for c in all_chunks]
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings, dtype=np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    
    index_path = os.path.join(data_dir, output_index_name)
    faiss.write_index(index, index_path)
    
    chunks_dict_list = [c.model_dump() for c in all_chunks]
    chunks_path = os.path.join(data_dir, output_chunks_name)
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks_dict_list, f, ensure_ascii=False, indent=2)

    return index, chunks_dict_list

if __name__ == "__main__":
    build_faiss_index()
