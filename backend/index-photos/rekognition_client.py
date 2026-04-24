def _boto3_client(service_name):
    import boto3

    return boto3.client(service_name)


def detect_labels(bucket, object_key):
    client = _boto3_client("rekognition")
    response = client.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": object_key}},
        MaxLabels=10,
    )
    return response.get("Labels", [])
