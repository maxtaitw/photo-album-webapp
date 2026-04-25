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
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
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
