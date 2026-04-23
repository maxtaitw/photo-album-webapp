import json
import unittest
from pathlib import Path

from rekognition_client import detect_labels


class RekognitionClientTest(unittest.TestCase):
    def test_detect_labels_reads_simulated_labels_from_event(self):
        event_path = Path(__file__).parent / "events" / "s3-put.json"
        event = json.loads(event_path.read_text())
        record = event["Records"][0]

        self.assertEqual(
            detect_labels(record),
            [{"Name": "Dog"}, {"Name": "Park"}, {"Name": "Sam"}],
        )


if __name__ == "__main__":
    unittest.main()
