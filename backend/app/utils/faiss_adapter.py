import os
import numpy as np
from typing import Tuple

try:
    import faiss as real_faiss
    FAISS_AVAILABLE = True
except ImportError:
    real_faiss = None
    FAISS_AVAILABLE = False

class NumPyIndexFlatIP:
    """High-speed pure NumPy cosine / inner-product index matching FAISS IndexFlatIP API."""
    def __init__(self, d: int):
        self.d = d
        self.vectors: np.ndarray = np.empty((0, d), dtype=np.float32)
        self.ntotal = 0

    def add(self, x: np.ndarray):
        x = np.asarray(x, dtype=np.float32)
        if len(x.shape) == 1:
            x = x.reshape(1, -1)
        if self.ntotal == 0:
            self.vectors = x.copy()
        else:
            self.vectors = np.vstack([self.vectors, x])
        self.ntotal = self.vectors.shape[0]

    def search(self, x: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        x = np.asarray(x, dtype=np.float32)
        if len(x.shape) == 1:
            x = x.reshape(1, -1)
        if self.ntotal == 0:
            return np.zeros((x.shape[0], 0), dtype=np.float32), np.zeros((x.shape[0], 0), dtype=np.int64)

        k = min(k, self.ntotal)
        # Inner product (cosine similarity since vectors are L2-normalized)
        sims = np.dot(x, self.vectors.T) # shape: (num_queries, ntotal)
        
        # Get top-k indices
        indices = np.argsort(-sims, axis=1)[:, :k]
        scores = np.take_along_axis(sims, indices, axis=1)
        
        return scores.astype(np.float32), indices.astype(np.int64)

class FaissProxy:
    def IndexFlatIP(self, d: int):
        if FAISS_AVAILABLE and real_faiss is not None:
            return real_faiss.IndexFlatIP(d)
        return NumPyIndexFlatIP(d)

    def write_index(self, index, filename: str):
        if FAISS_AVAILABLE and real_faiss is not None and hasattr(real_faiss, "write_index") and not isinstance(index, NumPyIndexFlatIP):
            return real_faiss.write_index(index, filename)
        # Save as npz
        np.savez_compressed(filename, vectors=index.vectors, d=index.d)

    def read_index(self, filename: str):
        if FAISS_AVAILABLE and real_faiss is not None and not filename.endswith(".npz"):
            try:
                return real_faiss.read_index(filename)
            except Exception:
                pass
        
        # Load from numpy
        data = np.load(filename if filename.endswith(".npz") or not os.path.exists(filename + ".npz") else filename + ".npz")
        idx = NumPyIndexFlatIP(d=int(data["d"]))
        idx.add(data["vectors"])
        return idx

faiss = FaissProxy()
