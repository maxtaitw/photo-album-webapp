import unittest

from search_client import search_photos


class SearchClientTest(unittest.TestCase):
    def test_search_photos_returns_empty_list_for_empty_keywords(self):
        self.assertEqual(search_photos([]), [])

    def test_search_photos_returns_single_match_for_one_keyword(self):
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

    def test_search_photos_returns_matching_photo_for_two_keywords(self):
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

    def test_search_photos_returns_empty_list_for_non_matching_keyword(self):
        self.assertEqual(search_photos(["bridge"]), [])


if __name__ == "__main__":
    unittest.main()
