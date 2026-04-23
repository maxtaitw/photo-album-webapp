import json
import unittest
from pathlib import Path

from handler import lambda_handler


class IndexPhotosHandlerTest(unittest.TestCase):
    def test_handler_builds_photo_documents_from_s3_event(self):
        event_path = Path(__file__).parent / "events" / "s3-put.json"
        event = json.loads(event_path.read_text())

        response = lambda_handler(event, None)
        body = json.loads(response["body"])

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
                        "labels": ["sam", "sally"],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
