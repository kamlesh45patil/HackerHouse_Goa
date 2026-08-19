from .base import BaseChunker
from .fixed_size import FixedSizeChunker
from .semantic import SemanticChunker
from .metadata_aware import MetadataAwareChunker

def get_chunker(strategy_name: str) -> BaseChunker:
    strategies = {
        "fixed": FixedSizeChunker(),
        "fixed_size": FixedSizeChunker(),
        "semantic": SemanticChunker(),
        "metadata_aware": MetadataAwareChunker(),
        "meta": MetadataAwareChunker()
    }
    if strategy_name not in strategies:
        raise ValueError(f"Unknown chunking strategy: {strategy_name}. Choose from {list(strategies.keys())}")
    return strategies[strategy_name]
