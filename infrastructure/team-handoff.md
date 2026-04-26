# Team Handoff

This file is for the teammate who will continue the project from the current deployed backend state.

## Done

- Backend is implemented in Python.
- `index-photos` Lambda is deployed and triggered by the photo S3 bucket.
- `search-photos` Lambda is deployed and callable from API Gateway.
- Rekognition label detection is working for uploaded images.
- Custom labels from `x-amz-meta-customLabels` are being read and merged into indexed labels.
- OpenSearch indexing and search are working.
- Lex is configured and returns search keywords for the current query flow.
- API Gateway `GET /search` is deployed and working with an API key.
- API Gateway `PUT /photos/{object}` is deployed and working with an API key.
- End-to-end validation succeeded for:
  - image upload through API Gateway
  - automatic Rekognition labels
  - custom labels such as `sam` and `sally`
  - search through the deployed API

## Todo

- Build the frontend UI in `frontend/`.
- Create and deploy the frontend S3 static website bucket.
- Add a basic CloudFormation template for submission.
- Clean up documentation for submission.
- Optional if time allows:
  - narrow IAM permissions
  - add deploy scripts
  - add CodePipeline

## Current Deployed Backend

- Region: `us-east-1`
- Photo bucket: `photo-album-storage-cc-hw3`
- OpenSearch domain: `photos`
- OpenSearch index: `photos`
- Lambda functions:
  - `index-photos`
  - `search-photos`
- API Gateway base URL:
  - `https://or7z11lo1g.execute-api.us-east-1.amazonaws.com/prod`

The current API key is shared separately and should not be committed to the repo.

## API Usage

### Search

```http
GET /search?q={query text}
x-api-key: <shared api key>
```

Example:

```bash
curl -H "x-api-key: <API_KEY>" \
  "https://or7z11lo1g.execute-api.us-east-1.amazonaws.com/prod/search?q=sam"
```

### Upload

```http
PUT /photos/{object}
x-api-key: <shared api key>
Content-Type: image/jpeg | image/png
x-amz-meta-customLabels: label one, label two
```

Example:

```bash
curl -X PUT \
  -H "x-api-key: <API_KEY>" \
  -H "Content-Type: image/jpeg" \
  -H "x-amz-meta-customLabels: Sam, Sally" \
  --data-binary @"/path/to/photo.jpg" \
  "https://or7z11lo1g.execute-api.us-east-1.amazonaws.com/prod/photos/demo-photo.jpg"
```

Important: `--data-binary` must use `@/path/to/file`. If the `@` is missing, curl uploads the path string instead of the image bytes.

## How The Backend Works

### Indexing flow

```text
PUT /photos/{object}
-> API Gateway
-> S3 photo bucket
-> S3 ObjectCreated trigger
-> index-photos Lambda
-> Rekognition DetectLabels
-> S3 head_object for metadata
-> merge Rekognition labels + custom labels
-> OpenSearch index "photos"
```

### Search flow

```text
GET /search?q=...
-> API Gateway
-> search-photos Lambda
-> Lex
-> OpenSearch search
-> JSON response
```

## Files That Matter

- `backend/index-photos/handler.py`
- `backend/index-photos/rekognition_client.py`
- `backend/index-photos/s3_metadata_client.py`
- `backend/index-photos/index_client.py`
- `backend/index-photos/photo_document.py`
- `backend/search-photos/handler.py`
- `backend/search-photos/lex_client.py`
- `backend/search-photos/search_client.py`
- `backend/search-photos/query_parser.py`
- `infrastructure/backend-deployment-checklist.md`

## Important Notes

### OpenSearch auth

The OpenSearch clients use AWS SigV4 signing. This was required because unsigned HTTP requests were rejected with `403 Forbidden`.

If OpenSearch access breaks, check:

1. Lambda execution role permissions
2. OpenSearch domain access policy
3. Whether request signing code was removed from:
   - `backend/index-photos/index_client.py`
   - `backend/search-photos/search_client.py`

### API Gateway binary uploads

Image uploads through API Gateway required binary media type support. Without it, S3 received corrupted image bodies and Rekognition failed with `InvalidImageFormatException`.

If uploads start failing again:

1. Check API Gateway binary media types for image content
2. Redeploy the API stage after API changes
3. Confirm the uploaded S3 object is a real image, not a text payload

### Custom label header

Continue using:

```http
x-amz-meta-customLabels
```

S3 stores user metadata keys in lowercase, so the Lambda reads back `customlabels` from `head_object`.

## What To Do Next

The main remaining work is frontend and submission artifacts.

Recommended order:

1. Build the frontend in `frontend/`
2. Wire the frontend to the deployed backend API
3. Create the frontend S3 website bucket and deploy the UI
4. Add the CloudFormation skeleton
5. Clean up documentation and collect final screenshots

## Frontend Expectations

The frontend should:

1. Search photos with `GET /search`
2. Upload photos with `PUT /photos/{object}`
3. Allow optional custom labels on upload
4. Display returned photo results

## Validation Checklist

- Upload an image without custom labels and confirm it is searchable by Rekognition labels.
- Upload an image with custom labels and confirm it is searchable by custom labels.
- Verify `GET /search` through API Gateway, not only Lambda console tests.
- Verify `PUT /photos/{object}` through API Gateway, not only S3 console uploads.
- Confirm the frontend can call the deployed API.

## Known Gaps

- Frontend is still not implemented in this repo.
- CloudFormation template is still missing.
- CodePipeline is still missing.
- Some AWS settings were created manually in the console and should be documented before submission.
