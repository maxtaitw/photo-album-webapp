# Backend

This folder will contain the Lambda functions for the photo album application.

Planned functions:

- [`index-photos`](index-photos/): handles S3 photo upload events, calls Rekognition, reads custom labels from S3 metadata, and writes searchable photo metadata to OpenSearch.
- [`search-photos`](search-photos/): handles API search requests, uses Lex to extract keywords, searches OpenSearch, and returns matching photos.

We will add the Lambda code incrementally after the AWS flow is clear.

## Build Order

1. Document each Lambda's input event, output behavior, and permissions.
2. Create minimal handler files without external dependencies.
3. Add local test events that represent S3 and API Gateway inputs.
4. Implement AWS SDK calls one service at a time.
5. Deploy to AWS only after the local handler shape is clear.

## Local Smoke Tests

The current Python handlers do not call AWS yet. They only parse sample Lambda events.

Run `index-photos` locally:

```sh
python -c "import json, sys; from pathlib import Path; sys.path.insert(0, 'backend/index-photos'); from handler import lambda_handler; event = json.loads(Path('backend/index-photos/events/s3-put.json').read_text()); print(json.dumps(lambda_handler(event, None), indent=2))"
```

Run `search-photos` locally:

```sh
python -c "import json, sys; from pathlib import Path; sys.path.insert(0, 'backend/search-photos'); from handler import lambda_handler; event = json.loads(Path('backend/search-photos/events/api-gateway-search.json').read_text()); print(json.dumps(lambda_handler(event, None), indent=2))"
```

Run `index-photos` tests from the repository root:

```sh
python backend/index-photos/test_photo_document.py
python backend/index-photos/test_handler.py
```
