def _normalize_label(label):
    return str(label).strip().lower()


def parse_custom_labels(value):
    if not value:
        return []

    return [
        label
        for label in (_normalize_label(part) for part in str(value).split(","))
        if label
    ]


def _normalize_rekognition_labels(labels):
    if not isinstance(labels, list):
        return []

    normalized = []
    for label in labels:
        if isinstance(label, str):
            value = label
        elif isinstance(label, dict):
            value = label.get("Name")
        else:
            value = None

        if value:
            normalized_label = _normalize_label(value)
            if normalized_label:
                normalized.append(normalized_label)

    return normalized


def merge_labels(rekognition_labels, custom_labels):
    merged = []
    seen = set()

    for label in [
        *_normalize_rekognition_labels(rekognition_labels),
        *parse_custom_labels(custom_labels),
    ]:
        if label not in seen:
            seen.add(label)
            merged.append(label)

    return merged


def build_photo_document(bucket, object_key, created_timestamp, labels):
    return {
        "objectKey": object_key,
        "bucket": bucket,
        "createdTimestamp": created_timestamp,
        "labels": labels,
    }
