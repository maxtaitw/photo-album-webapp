import unittest

from query_parser import extract_keywords, normalize_query


class QueryParserTest(unittest.TestCase):
    def test_normalize_query(self):
        self.assertEqual(normalize_query("  Show Me Trees  "), "show me trees")
        self.assertEqual(normalize_query(""), "")
        self.assertEqual(normalize_query(None), "")

    def test_extract_keywords_from_single_keyword_query(self):
        self.assertEqual(extract_keywords("trees"), ["trees"])

    def test_extract_keywords_from_sentence_query(self):
        self.assertEqual(extract_keywords("show me trees"), ["trees"])
        self.assertEqual(
            extract_keywords("show me photos with trees and birds in them"),
            ["trees", "birds"],
        )

    def test_extract_keywords_deduplicates_and_limits_results(self):
        self.assertEqual(
            extract_keywords("show me dogs and dogs and parks and birds"),
            ["dogs", "parks"],
        )

    def test_extract_keywords_handles_empty_input(self):
        self.assertEqual(extract_keywords(""), [])
        self.assertEqual(extract_keywords(None), [])


if __name__ == "__main__":
    unittest.main()
