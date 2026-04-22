import json
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    records = event.get("Records", [])

    photos = []
    for record in records:
        s3_info = record.get("s3", {})
        bucket = s3_info.get("bucket", {}).get("name")
        object_key = s3_info.get("object", {}).get("key")

        photos.append(
            {
                "bucket": bucket,
                "objectKey": unquote_plus(object_key) if object_key else None,
                "eventTime": record.get("eventTime"),
            }
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
