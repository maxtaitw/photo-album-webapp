import json
from urllib.parse import unquote_plus

from photo_document import build_photo_document, merge_labels


def lambda_handler(event, context):
    records = event.get("Records", [])

    photos = []
    for record in records:
        s3_info = record.get("s3", {})
        bucket = s3_info.get("bucket", {}).get("name")
        s3_object = s3_info.get("object", {})
        object_key = s3_object.get("key")
        custom_labels = s3_object.get("metadata", {}).get("customLabels")
        rekognition_labels = s3_object.get("rekognitionLabels", [])

        photos.append(
            build_photo_document(
                bucket=bucket,
                object_key=unquote_plus(object_key) if object_key else None,
                created_timestamp=record.get("eventTime"),
                labels=merge_labels(rekognition_labels, custom_labels),
            )
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "index-photos handler received S3 upload event",
                "photos": photos,
            }
        ),
    }
