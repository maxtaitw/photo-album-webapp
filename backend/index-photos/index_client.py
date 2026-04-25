import json
import os
from urllib.request import Request, urlopen


def _get_index_config():
    endpoint = os.environ.get("OPENSEARCH_ENDPOINT")
    if not endpoint:
        raise RuntimeError("Missing OpenSearch configuration: OPENSEARCH_ENDPOINT")

    return {
        "endpoint": endpoint.rstrip("/"),
        "index": os.environ.get("OPENSEARCH_INDEX", "photos"),
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


def index_photo(document):
    config = _get_index_config()
    _post_json(f"{config['endpoint']}/{config['index']}/_doc", document)
    return document
