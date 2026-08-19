from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models.schemas import Chunk, ChunkMetadata

class BaseChunker(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def chunk_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Split document text into a list of Chunk objects."""
        pass
