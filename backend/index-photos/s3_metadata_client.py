def _boto3_client(service_name):
    import boto3

    return boto3.client(service_name)


def get_custom_labels(bucket, object_key):
    client = _boto3_client("s3")
    response = client.head_object(Bucket=bucket, Key=object_key)
    metadata = response.get("Metadata", {})
    return metadata.get("customlabels")
