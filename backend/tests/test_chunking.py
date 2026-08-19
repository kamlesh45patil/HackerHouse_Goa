import unittest
import os
import sys

# Ensure backend root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.chunking.fixed_size import FixedSizeChunker
from app.chunking.semantic import SemanticChunker
from app.chunking.metadata_aware import MetadataAwareChunker

SAMPLE_TEXT = (
    "Goa is famous for its beaches. North Goa has Baga and Calangute. "
    "South Goa has Palolem and Agonda. The Dudhsagar Falls is also a major attraction."
)

class TestChunkingStrategies(unittest.TestCase):
    def test_fixed_size_chunker(self):
        chunker = FixedSizeChunker(chunk_size=10, overlap=3)
        chunks = chunker.chunk_document(doc_id="doc_1", text=SAMPLE_TEXT)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertTrue(all(c.metadata.strategy == "fixed_size" for c in chunks))
        self.assertTrue(all(c.id.startswith("doc_1_fixed_") for c in chunks))

    def test_semantic_chunker(self):
        chunker = SemanticChunker(min_chunk_words=5, max_chunk_words=20)
        chunks = chunker.chunk_document(doc_id="doc_2", text=SAMPLE_TEXT)
        self.assertGreaterEqual(len(chunks), 1)
        self.assertTrue(all(c.metadata.strategy == "semantic" for c in chunks))

    def test_metadata_aware_chunker(self):
        chunker = MetadataAwareChunker(prepend_metadata=True)
        meta = {"lang": "hi", "query_type": "travel", "is_selected": 1}
        chunks = chunker.chunk_document(doc_id="doc_3", text=SAMPLE_TEXT, metadata=meta)
        self.assertEqual(len(chunks), 1)
        self.assertIn("[Lang: HI]", chunks[0].text)
        self.assertIn("[Topic: travel]", chunks[0].text)
        self.assertIn("[Verified Source]", chunks[0].text)

if __name__ == "__main__":
    unittest.main()
