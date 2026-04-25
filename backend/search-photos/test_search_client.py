import os
import unittest
from unittest.mock import patch

from search_client import search_photos


class SearchClientTest(unittest.TestCase):
    def test_search_photos_returns_empty_list_for_empty_keywords(self):
        self.assertEqual(search_photos([]), [])

    @patch.dict(
        os.environ,
        {
            "OPENSEARCH_ENDPOINT": "https://search.example.com",
            "OPENSEARCH_INDEX": "photos",
        },
        clear=True,
    )
    @patch("search_client._post_json")
    def test_search_photos_builds_query_and_returns_single_match(self, mock_post_json):
        mock_post_json.return_value = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "objectKey": "sample-photo.jpg",
                            "bucket": "photo-album-storage-bucket",
                            "createdTimestamp": "2026-04-22T12:40:02.000Z",
                            "labels": ["dog", "park", "sam", "sally"],
                        }
                    }
                ]
            }
        }

        self.assertEqual(
            search_photos(["dog"]),
            [
                {
                    "objectKey": "sample-photo.jpg",
                    "bucket": "photo-album-storage-bucket",
                    "createdTimestamp": "2026-04-22T12:40:02.000Z",
                    "labels": ["dog", "park", "sam", "sally"],
                }
            ],
        )
        mock_post_json.assert_called_once_with(
            "https://search.example.com/photos/_search",
            {
                "query": {
                    "bool": {
                        "should": [{"term": {"labels": "dog"}}],
                        "minimum_should_match": 1,
                    }
                }
            },
        )

    @patch.dict(
        os.environ,
        {
            "OPENSEARCH_ENDPOINT": "https://search.example.com",
            "OPENSEARCH_INDEX": "photos",
        },
        clear=True,
    )
    @patch("search_client._post_json")
    def test_search_photos_returns_matching_photo_for_two_keywords(self, mock_post_json):
        mock_post_json.return_value = {
            "hits": {
                "hits": [
                    {
                        "_source": {
                            "objectKey": "forest-birds.jpg",
                            "bucket": "photo-album-storage-bucket",
                            "createdTimestamp": "2026-04-23T09:15:00.000Z",
                            "labels": ["trees", "birds", "forest"],
                        }
                    }
                ]
            }
        }

        self.assertEqual(
            search_photos(["trees", "birds"]),
            [
                {
                    "objectKey": "forest-birds.jpg",
                    "bucket": "photo-album-storage-bucket",
                    "createdTimestamp": "2026-04-23T09:15:00.000Z",
                    "labels": ["trees", "birds", "forest"],
                }
            ],
        )

    @patch.dict(
        os.environ,
        {
            "OPENSEARCH_ENDPOINT": "https://search.example.com",
            "OPENSEARCH_INDEX": "photos",
        },
        clear=True,
    )
    @patch("search_client._post_json")
    def test_search_photos_returns_empty_list_for_non_matching_keyword(
        self, mock_post_json
    ):
        mock_post_json.return_value = {"hits": {"hits": []}}
        self.assertEqual(search_photos(["bridge"]), [])

    @patch.dict(os.environ, {}, clear=True)
    def test_search_photos_requires_opensearch_endpoint(self):
        with self.assertRaisesRegex(
            RuntimeError, "Missing OpenSearch configuration"
        ):
            search_photos(["trees"])


if __name__ == "__main__":
    unittest.main()
