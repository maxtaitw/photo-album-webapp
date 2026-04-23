import unittest

from index_client import index_photo


class IndexClientTest(unittest.TestCase):
    def test_index_photo_returns_document_unchanged_in_local_mode(self):
        document = {
            "objectKey": "sample-photo.jpg",
            "bucket": "photo-album-storage-bucket",
            "createdTimestamp": "2026-04-22T12:40:02.000Z",
            "labels": ["dog", "park", "sam", "sally"],
        }

        self.assertEqual(index_photo(document), document)


if __name__ == "__main__":
    unittest.main()
