import unittest
from unittest.mock import Mock, patch

from rekognition_client import detect_labels


class RekognitionClientTest(unittest.TestCase):
    @patch("rekognition_client._boto3_client")
    def test_detect_labels_calls_rekognition_and_returns_labels(self, mock_boto3_client):
        client = Mock()
        client.detect_labels.return_value = {
            "Labels": [{"Name": "Dog"}, {"Name": "Park"}, {"Name": "Sam"}]
        }
        mock_boto3_client.return_value = client

        labels = detect_labels("photo-album-storage-bucket", "sample-photo.jpg")

        mock_boto3_client.assert_called_once_with("rekognition")
        client.detect_labels.assert_called_once_with(
            Image={
                "S3Object": {
                    "Bucket": "photo-album-storage-bucket",
                    "Name": "sample-photo.jpg",
                }
            },
            MaxLabels=10,
        )
        self.assertEqual(labels, [{"Name": "Dog"}, {"Name": "Park"}, {"Name": "Sam"}])


if __name__ == "__main__":
    unittest.main()
