import os
import unittest
from unittest.mock import patch

from index_client import index_photo


class IndexClientTest(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "OPENSEARCH_ENDPOINT": "https://search.example.com",
            "OPENSEARCH_INDEX": "photos",
        },
        clear=True,
    )
    @patch("index_client._post_json")
    def test_index_photo_posts_document_and_returns_it(self, mock_post_json):
        document = {
            "objectKey": "sample-photo.jpg",
            "bucket": "photo-album-storage-bucket",
            "createdTimestamp": "2026-04-22T12:40:02.000Z",
            "labels": ["dog", "park", "sam", "sally"],
        }

        self.assertEqual(index_photo(document), document)
        mock_post_json.assert_called_once_with(
            "https://search.example.com/photos/_doc",
            document,
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_index_photo_requires_opensearch_endpoint(self):
        document = {
            "objectKey": "sample-photo.jpg",
            "bucket": "photo-album-storage-bucket",
            "createdTimestamp": "2026-04-22T12:40:02.000Z",
            "labels": ["dog", "park", "sam", "sally"],
        }

        with self.assertRaisesRegex(
            RuntimeError, "Missing OpenSearch configuration"
        ):
            index_photo(document)


if __name__ == "__main__":
    unittest.main()
