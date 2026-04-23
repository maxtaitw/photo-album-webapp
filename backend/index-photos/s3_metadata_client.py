def get_custom_labels(record):
    return record.get("s3", {}).get("object", {}).get("metadata", {}).get(
        "customLabels"
    )
