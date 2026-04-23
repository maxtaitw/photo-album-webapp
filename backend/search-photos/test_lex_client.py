import unittest

from lex_client import interpret_query


class LexClientTest(unittest.TestCase):
    def test_interpret_query_with_single_keyword(self):
        self.assertEqual(interpret_query("trees"), ["trees"])

    def test_interpret_query_with_sentence(self):
        self.assertEqual(interpret_query("show me trees"), ["trees"])
        self.assertEqual(
            interpret_query("show me photos with trees and birds in them"),
            ["trees", "birds"],
        )

    def test_interpret_query_with_empty_input(self):
        self.assertEqual(interpret_query(""), [])
        self.assertEqual(interpret_query(None), [])


if __name__ == "__main__":
    unittest.main()
