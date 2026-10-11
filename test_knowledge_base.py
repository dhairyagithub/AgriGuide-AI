import unittest
from knowledge_base import retrieve_context, SOURCES


class KnowledgeBaseTests(unittest.TestCase):
    def test_moisture_query_returns_relevant_context(self):
        docs = retrieve_context("soil moisture rainfall and hot weather", top_k=3)
        self.assertTrue(docs)
        self.assertTrue(
            any("weather" in doc["keywords"] or "moisture" in doc["keywords"]
                for doc in docs)
        )

    def test_growth_stage_query_returns_stage_context(self):
        docs = retrieve_context("grand growth stage irrigation interval", top_k=3)
        self.assertTrue(docs)
        self.assertTrue(any(doc["id"] == "tnau_stages" for doc in docs))

    def test_sources_have_urls(self):
        self.assertTrue(SOURCES)
        self.assertTrue(all(source["url"].startswith("https://") for source in SOURCES))


if __name__ == "__main__":
    unittest.main()
