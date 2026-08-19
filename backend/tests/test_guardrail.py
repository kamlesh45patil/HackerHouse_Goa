import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline.guardrail import GuardrailService
from app.models.schemas import CitedChunk

class TestGuardrailService(unittest.TestCase):
    def test_guardrail_pre_check_safe(self):
        guard = GuardrailService()
        res = guard.pre_check("What are the best beaches in Goa?")
        self.assertTrue(res.passed)
        self.assertTrue(res.is_safe)

    def test_guardrail_pre_check_unsafe(self):
        guard = GuardrailService()
        res = guard.pre_check("How to make a bomb and attack a website?")
        self.assertFalse(res.passed)
        self.assertFalse(res.is_safe)
        self.assertIn("unsafe", res.reason.lower())

    def test_guardrail_post_grounding(self):
        guard = GuardrailService(grounding_threshold=0.2)
        chunks = [
            CitedChunk(
                id="c1",
                text="Baga and Calangute are popular beaches in North Goa.",
                score=0.9,
                doc_id="1",
                lang="en",
                strategy="fixed"
            )
        ]
        res = guard.post_grounding_check("Baga is a well-known beach in Goa.", chunks)
        self.assertTrue(res.is_grounded)

if __name__ == "__main__":
    unittest.main()
