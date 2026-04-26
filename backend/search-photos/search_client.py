import json
import os
from urllib.request import Request, urlopen


def _get_search_config():
    endpoint = os.environ.get("OPENSEARCH_ENDPOINT")
    if not endpoint:
        raise RuntimeError("Missing OpenSearch configuration: OPENSEARCH_ENDPOINT")

    return {
        "endpoint": endpoint.rstrip("/"),
        "index": os.environ.get("OPENSEARCH_INDEX", "photos"),
    }


def _build_sigv4_headers(url, body):
    import boto3
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest

    session = boto3.Session()
    credentials = session.get_credentials()
    if credentials is None:
        raise RuntimeError("Missing AWS credentials for OpenSearch request signing")

    frozen_credentials = credentials.get_frozen_credentials()
    region = (
        session.region_name
        or os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    request = AWSRequest(
        method="POST",
        url=url,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    SigV4Auth(frozen_credentials, "es", region).add_auth(request)
    return dict(request.headers.items())


def _build_query(keywords):
    return {
        "query": {
            "bool": {
                "should": [{"term": {"labels": keyword}} for keyword in keywords],
                "minimum_should_match": 1,
            }
        }
    }


def _post_json(url, payload):
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers=_build_sigv4_headers(url, body),
        method="POST",
    )
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def _map_hit_to_photo(hit):
    source = hit.get("_source", {})
    return {
        "objectKey": source.get("objectKey"),
        "bucket": source.get("bucket"),
        "createdTimestamp": source.get("createdTimestamp"),
        "labels": source.get("labels", []),
    }


def search_photos(keywords):
    if not keywords:
        return []

    config = _get_search_config()
    query = _build_query(keywords)
    response = _post_json(
        f"{config['endpoint']}/{config['index']}/_search",
        query,
    )

    hits = ((response.get("hits") or {}).get("hits")) or []
    return [_map_hit_to_photo(hit) for hit in hits]
