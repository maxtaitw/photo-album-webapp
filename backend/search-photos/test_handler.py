import json
import unittest
from pathlib import Path

from handler import lambda_handler


class SearchPhotosHandlerTest(unittest.TestCase):
    def test_handler_returns_query_keywords_and_matching_results(self):
        event_path = Path(__file__).parent / "events" / "api-gateway-search.json"
        event = json.loads(event_path.read_text())

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["headers"], {"Content-Type": "application/json"})
        self.assertEqual(
            body,
            {
                "query": "show me photos with trees and birds",
                "keywords": ["trees", "birds"],
                "results": [
                    {
                        "objectKey": "forest-birds.jpg",
                        "bucket": "photo-album-storage-bucket",
                        "createdTimestamp": "2026-04-23T09:15:00.000Z",
                        "labels": ["trees", "birds", "forest"],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
