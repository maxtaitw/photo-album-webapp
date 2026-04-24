import json
import unittest
from pathlib import Path
from unittest.mock import patch

from handler import lambda_handler


class IndexPhotosHandlerTest(unittest.TestCase):
    @patch("handler.index_photo")
    @patch("handler.get_custom_labels")
    @patch("handler.detect_labels")
    def test_handler_builds_photo_documents_from_s3_event(
        self, mock_detect_labels, mock_get_custom_labels, mock_index_photo
    ):
        event_path = Path(__file__).parent / "events" / "s3-put.json"
        event = json.loads(event_path.read_text())
        mock_detect_labels.return_value = [
            {"Name": "Dog"},
            {"Name": "Park"},
            {"Name": "Sam"},
        ]
        mock_get_custom_labels.return_value = "Sam, Sally"
        mock_index_photo.side_effect = lambda document: document

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

        mock_detect_labels.assert_called_once_with(
            "photo-album-storage-bucket", "sample-photo.jpg"
        )
        mock_get_custom_labels.assert_called_once_with(
            "photo-album-storage-bucket", "sample-photo.jpg"
        )
        mock_index_photo.assert_called_once()
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            body,
            {
                "message": "index-photos handler received S3 upload event",
                "photos": [
                    {
                        "objectKey": "sample-photo.jpg",
                        "bucket": "photo-album-storage-bucket",
                        "createdTimestamp": "2026-04-22T12:40:02.000Z",
                        "labels": ["dog", "park", "sam", "sally"],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
