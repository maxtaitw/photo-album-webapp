import unittest

from photo_document import build_photo_document, merge_labels, parse_custom_labels


class PhotoDocumentTest(unittest.TestCase):
    def test_parse_custom_labels(self):
        self.assertEqual(parse_custom_labels("Sam, Sally"), ["sam", "sally"])
        self.assertEqual(parse_custom_labels("  Sam  , , Sally "), ["sam", "sally"])
        self.assertEqual(parse_custom_labels(""), [])
        self.assertEqual(parse_custom_labels(None), [])

    def test_merge_labels_from_rekognition_and_custom_metadata(self):
        self.assertEqual(
            merge_labels([{"Name": "Dog"}, {"Name": "Park"}], "dog, Ball"),
            ["dog", "park", "ball"],
        )

    def test_merge_labels_accepts_string_labels_and_removes_duplicates(self):
        self.assertEqual(
            merge_labels(["Tree", "tree", "Bird"], "bird, sky"),
            ["tree", "bird", "sky"],
        )

    def test_build_photo_document_matches_assignment_shape(self):
        self.assertEqual(
            build_photo_document(
                bucket="photo-album-storage-bucket",
                object_key="sample-photo.jpg",
                created_timestamp="2026-04-22T12:40:02.000Z",
                labels=["tree", "bird"],
            ),
            {
                "objectKey": "sample-photo.jpg",
                "bucket": "photo-album-storage-bucket",
                "createdTimestamp": "2026-04-22T12:40:02.000Z",
                "labels": ["tree", "bird"],
            },
        )


if __name__ == "__main__":
    unittest.main()
