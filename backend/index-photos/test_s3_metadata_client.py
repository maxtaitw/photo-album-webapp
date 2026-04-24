import unittest
from unittest.mock import Mock, patch

from s3_metadata_client import get_custom_labels


class S3MetadataClientTest(unittest.TestCase):
    @patch("s3_metadata_client._boto3_client")
    def test_get_custom_labels_reads_s3_metadata(self, mock_boto3_client):
        client = Mock()
        client.head_object.return_value = {"Metadata": {"customlabels": "Sam, Sally"}}
        mock_boto3_client.return_value = client

        custom_labels = get_custom_labels(
            "photo-album-storage-bucket", "sample-photo.jpg"
        )

        mock_boto3_client.assert_called_once_with("s3")
        client.head_object.assert_called_once_with(
            Bucket="photo-album-storage-bucket",
            Key="sample-photo.jpg",
        )
        self.assertEqual(custom_labels, "Sam, Sally")


if __name__ == "__main__":
    unittest.main()
