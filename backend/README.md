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

The current handlers do not call AWS yet. They only parse sample Lambda events.

Run `index-photos` locally:

```sh
node -e "const event = require('./index-photos/events/s3-put.json'); require('./index-photos').handler(event).then(console.log)"
```

Run `search-photos` locally:

```sh
node -e "const event = require('./search-photos/events/api-gateway-search.json'); require('./search-photos').handler(event).then(console.log)"
```
