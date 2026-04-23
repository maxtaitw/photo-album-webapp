def detect_labels(record):
    return record.get("s3", {}).get("object", {}).get("rekognitionLabels", [])
