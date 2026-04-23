import json
import unittest
from pathlib import Path

from s3_metadata_client import get_custom_labels


class S3MetadataClientTest(unittest.TestCase):
    def test_get_custom_labels_reads_simulated_metadata_from_event(self):
        event_path = Path(__file__).parent / "events" / "s3-put.json"
        event = json.loads(event_path.read_text())
        record = event["Records"][0]

        self.assertEqual(get_custom_labels(record), "Sam, Sally")


if __name__ == "__main__":
    unittest.main()
