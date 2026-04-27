import json
import unittest
from pathlib import Path
from unittest.mock import patch

from handler import lambda_handler


class SearchPhotosHandlerTest(unittest.TestCase):
    @patch("handler.search_photos")
    @patch("handler.interpret_query")
    def test_handler_returns_query_keywords_and_matching_results(
        self, mock_interpret_query, mock_search_photos
    ):
        event_path = Path(__file__).parent / "events" / "api-gateway-search.json"
        event = json.loads(event_path.read_text())
        mock_interpret_query.return_value = ["trees", "birds"]
        mock_search_photos.return_value = [
            {
                "objectKey": "forest-birds.jpg",
                "bucket": "photo-album-storage-bucket",
                "url": "https://photo-album-storage-bucket.s3.us-east-1.amazonaws.com/forest-birds.jpg",
                "createdTimestamp": "2026-04-23T09:15:00.000Z",
                "labels": ["trees", "birds", "forest"],
            }
        ]

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        mock_interpret_query.assert_called_once_with("show me photos with trees and birds")
        mock_search_photos.assert_called_once_with(["trees", "birds"])
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            response["headers"],
            {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
            },
        )
        self.assertEqual(
            body,
            {
                "query": "show me photos with trees and birds",
                "keywords": ["trees", "birds"],
                "results": [
                    {
                        "objectKey": "forest-birds.jpg",
                        "bucket": "photo-album-storage-bucket",
                        "url": "https://photo-album-storage-bucket.s3.us-east-1.amazonaws.com/forest-birds.jpg",
                        "createdTimestamp": "2026-04-23T09:15:00.000Z",
                        "labels": ["trees", "birds", "forest"],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
