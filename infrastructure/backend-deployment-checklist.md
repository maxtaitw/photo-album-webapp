# Backend Deployment Checklist

This checklist turns the current local backend into a real AWS-backed backend.

## 1. Create AWS Resources

Create these resources manually in AWS first:

- S3 photo storage bucket
- OpenSearch domain
- Lex V2 bot
- Lex V2 bot alias
- Two Lambda functions:
  - `index-photos`
  - `search-photos`

Recommended naming pattern:

- S3 bucket: `photo-album-storage-<unique-suffix>`
- OpenSearch index: `photos`
- Lambda names:
  - `index-photos`
  - `search-photos`

## 2. Lambda Runtime

Use Python for both Lambdas.

Recommended Lambda settings:

- Runtime: Python 3.12 if available, otherwise the newest supported Python runtime in your account
- Architecture: x86_64
- Timeout:
  - `index-photos`: 30 seconds
  - `search-photos`: 15 seconds

## 3. Environment Variables

Set these for `index-photos`:

```text
OPENSEARCH_ENDPOINT=<your-opensearch-endpoint>
OPENSEARCH_INDEX=photos
```

Set these for `search-photos`:

```text
LEX_BOT_ID=<your-lex-bot-id>
LEX_BOT_ALIAS_ID=<your-lex-bot-alias-id>
LEX_LOCALE_ID=en_US
OPENSEARCH_ENDPOINT=<your-opensearch-endpoint>
OPENSEARCH_INDEX=photos
```

## 4. IAM Permissions

`index-photos` execution role needs:

- `rekognition:DetectLabels`
- `s3:HeadObject` on the photo bucket
- OpenSearch write access
- CloudWatch Logs write access

`search-photos` execution role needs:

- Lex V2 runtime access
- OpenSearch read access
- CloudWatch Logs write access

## 5. Upload Backend Code

Deploy `index-photos` from:

- `backend/index-photos/handler.py`

Lambda handler value:

```text
handler.lambda_handler
```

Deploy `search-photos` from:

- `backend/search-photos/handler.py`

Lambda handler value:

```text
handler.lambda_handler
```

When packaging each Lambda, include the Python files from that Lambda folder together.

## 6. Configure Event Sources

For `index-photos`:

- Add an S3 `PUT` trigger from the photo bucket

For `search-photos`:

- No trigger yet
- This Lambda will be invoked later from API Gateway

## 7. Create the OpenSearch Index

Create or allow first-write creation of the `photos` index.

Expected document shape:

```json
{
  "objectKey": "sample-photo.jpg",
  "bucket": "photo-album-storage-bucket",
  "createdTimestamp": "2026-04-22T12:40:02.000Z",
  "labels": ["dog", "park", "sam", "sally"]
}
```

## 8. Create and Test Lex V2

Create:

- one bot
- one alias
- locale `en_US`
- one intent: `SearchIntent`

Add utterances that cover:

- `trees`
- `birds`
- `show me trees`
- `show me photos with trees and birds in them`

Make sure the bot returns one or two extracted search terms that your Lambda can read from slots.

## 9. Test Order

Test in this order:

1. Upload one image to the photo S3 bucket without custom labels
2. Confirm `index-photos` runs
3. Upload one image with `x-amz-meta-customLabels`
4. Confirm the Lambda reads custom labels
5. Confirm OpenSearch receives the indexed document
6. Invoke `search-photos` manually with a known query
7. Confirm Lex returns keywords
8. Confirm OpenSearch search returns matching photos

## 10. What Comes Next

After the backend works in AWS:

1. API Gateway
2. Frontend upload/search UI
3. CloudFormation template
4. CodePipeline
