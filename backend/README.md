# Backend

This folder will contain the Lambda functions for the photo album application.

Planned functions:

- `index-photos`: handles S3 photo upload events, calls Rekognition, reads custom labels from S3 metadata, and writes searchable photo metadata to OpenSearch.
- `search-photos`: handles API search requests, uses Lex to extract keywords, searches OpenSearch, and returns matching photos.

We will add the Lambda code incrementally after the AWS flow is clear.
