from typing import List, Dict, Any, Optional
from .base import BaseChunker
from ..models.schemas import Chunk, ChunkMetadata

class MetadataAwareChunker(BaseChunker):
    """
    Strategy 3: Metadata-Aware Chunking.
    Keeps logical passage units intact and enriches each passage with structured
    metadata headers (e.g. language, query domain/type, source doc ID, gold relevance tag).
    This contextual prefix enables dense retrievers to match semantic domain & cross-lingual intent.
    """
    def __init__(self, prepend_metadata: bool = True):
        super().__init__(name="metadata_aware")
        self.prepend_metadata = prepend_metadata

    def chunk_document(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        meta = metadata or {}
        lang = meta.get("lang", "en")
        query_type = meta.get("query_type", "general")
        passage_idx = meta.get("passage_idx", 0)
        is_selected = meta.get("is_selected", 0)
        source_url = meta.get("url", "")

        # Format contextual header
        prefix_parts = []
        if lang:
            prefix_parts.append(f"[Lang: {lang.upper()}]")
        if query_type:
            prefix_parts.append(f"[Topic: {query_type}]")
        if is_selected == 1:
            prefix_parts.append("[Verified Source]")
        
        prefix = " ".join(prefix_parts) + " " if (self.prepend_metadata and prefix_parts) else ""
        enriched_text = f"{prefix}{text.strip()}"

        chunk_id = f"{doc_id}_meta_{passage_idx}"
        chunk_meta = ChunkMetadata(
            doc_id=doc_id,
            passage_idx=passage_idx,
            lang=lang,
            query_type=query_type,
            is_selected=is_selected,
            strategy="metadata_aware",
            start_char=0,
            end_char=len(enriched_text),
            token_count=len(enriched_text.split()),
            extra={"source_url": source_url, "prefix": prefix}
        )

        return [Chunk(id=chunk_id, text=enriched_text, score=0.0, metadata=chunk_meta)]
