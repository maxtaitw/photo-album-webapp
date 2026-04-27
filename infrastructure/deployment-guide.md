# Deployment Guide

This guide assumes the backend in `team-handoff.md` is already deployed in `us-east-1`.

## 1. Put the API key in the frontend config

Do not commit the API key.

```bash
cd photo-album-webapp
cp frontend/config.example.js frontend/config.js
```

Edit `frontend/config.js` and replace `PUT_YOUR_SHARED_API_KEY_HERE` with the key from your teammate.

## 2. Redeploy the updated search Lambda

This repo change adds CORS headers and a `url` field in search results. Package and upload the function code:

```bash
cd photo-album-webapp/backend/search-photos
zip -j /tmp/search-photos.zip *.py
aws lambda update-function-code \
  --function-name search-photos \
  --zip-file fileb:///tmp/search-photos.zip \
  --region us-east-1
```

Set this optional environment variable if the photo bucket is not in `us-east-1`:

```bash
aws lambda update-function-configuration \
  --function-name search-photos \
  --environment "Variables={LEX_BOT_ID=<bot-id>,LEX_BOT_ALIAS_ID=<alias-id>,LEX_LOCALE_ID=en_US,OPENSEARCH_ENDPOINT=<endpoint>,OPENSEARCH_INDEX=photos,PHOTO_BUCKET_REGION=us-east-1}" \
  --region us-east-1
```

Keep the existing real values when updating the environment.

## 3. Confirm API Gateway browser settings

The frontend sends these browser requests:

- `GET /search?q=<query>` with `x-api-key`
- `PUT /photos/<object>` with `x-api-key`, `Content-Type`, and optional `x-amz-meta-customLabels`

In API Gateway, confirm:

- `GET /search` has API key required.
- `PUT /photos/{object}` has API key required.
- Binary media types include `image/jpeg`, `image/jpg`, and `image/png`.
- CORS/OPTIONS allows origin `*`, methods `GET,PUT,OPTIONS`, and headers `Content-Type,x-api-key,x-amz-meta-customLabels`.
- The API is redeployed to the `prod` stage after any change.

## 4. Make photo objects readable by the frontend

The frontend displays search results using `photo.url`, or by constructing:

```text
https://<bucket>.s3.<region>.amazonaws.com/<objectKey>
```

For the course project, the simplest setup is allowing public `s3:GetObject` on the photo bucket. If you do not make uploaded photo objects readable, searches can still work but the browser cannot display the images.

## 5. Deploy the frontend S3 website

Create a unique bucket name:

```bash
FRONTEND_BUCKET=photo-album-frontend-<your-unique-suffix>
aws s3 mb s3://$FRONTEND_BUCKET --region us-east-1
aws s3 website s3://$FRONTEND_BUCKET --index-document index.html --error-document index.html
```

Disable block public access for the frontend bucket, then attach a public read policy:

```bash
aws s3api put-public-access-block \
  --bucket $FRONTEND_BUCKET \
  --public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false
```

Copy the example policy and replace `REPLACE_WITH_FRONTEND_BUCKET_NAME` with your bucket name:

```bash
cp infrastructure/frontend-bucket-policy.example.json infrastructure/frontend-bucket-policy.json
```

```bash
aws s3api put-bucket-policy \
  --bucket $FRONTEND_BUCKET \
  --policy file://infrastructure/frontend-bucket-policy.json
```

If you do not use the JSON file, create an equivalent policy that allows public `s3:GetObject` on `arn:aws:s3:::$FRONTEND_BUCKET/*`.

Upload the frontend files:

```bash
aws s3 sync frontend/ s3://$FRONTEND_BUCKET/ \
  --exclude "README.md" \
  --exclude "config.example.js"
```

Open:

```text
http://$FRONTEND_BUCKET.s3-website-us-east-1.amazonaws.com
```

## 6. Deploy the CloudFormation template for submission

The assignment says the template only needs to create both Lambdas, API Gateway, and both S3 buckets. OpenSearch and CodePipeline are not required inside this template.

Create a deployment artifact bucket and upload Lambda zips:

```bash
ARTIFACT_BUCKET=photo-album-artifacts-<your-unique-suffix>
aws s3 mb s3://$ARTIFACT_BUCKET --region us-east-1

cd photo-album-webapp
zip -j /tmp/index-photos.zip backend/index-photos/*.py
zip -j /tmp/search-photos.zip backend/search-photos/*.py
aws s3 cp /tmp/index-photos.zip s3://$ARTIFACT_BUCKET/lambda/index-photos.zip
aws s3 cp /tmp/search-photos.zip s3://$ARTIFACT_BUCKET/lambda/search-photos.zip
```

Create the stack:

```bash
aws cloudformation deploy \
  --stack-name photo-album-assignment3 \
  --template-file infrastructure/cloudformation-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    PhotoBucketName=photo-album-storage-<your-unique-suffix> \
    FrontendBucketName=photo-album-frontend-<your-unique-suffix> \
    LambdaCodeBucket=$ARTIFACT_BUCKET \
    OpenSearchEndpoint=<your-existing-opensearch-endpoint> \
    LexBotId=<your-lex-bot-id> \
    LexBotAliasId=<your-lex-bot-alias-id> \
  --region us-east-1
```

Get outputs:

```bash
aws cloudformation describe-stacks \
  --stack-name photo-album-assignment3 \
  --query "Stacks[0].Outputs" \
  --region us-east-1
```

## 7. CodePipeline submission path

The PDF lists CodePipeline as required acceptance criteria, even though the handoff called it optional. The fastest acceptable setup is:

- Pipeline P1: GitHub source -> CodeBuild using `infrastructure/buildspec-backend.yml` -> deploys both Lambda functions.
- Pipeline P2: GitHub source -> CodeBuild using `infrastructure/buildspec-frontend.yml` -> syncs `frontend/` to the frontend S3 bucket.

For P2, configure CodeBuild environment variables:

- `FRONTEND_BUCKET`: your frontend S3 bucket name.
- `API_BASE_URL`: API Gateway base URL.
- `PHOTO_ALBUM_API_KEY`: the key from your teammate.
- `AWS_REGION`: `us-east-1`.
- `PHOTO_BASE_URL`: optional public base URL for photo objects.

Do not store `PHOTO_ALBUM_API_KEY` in the repo. Use a CodeBuild secret environment variable or Secrets Manager.

## 8. Final validation

Run these checks before submission:

- Upload an image without custom labels, then search by a Rekognition label.
- Upload an image with `Sam, Sally`, then search for `Sam` and `Sally`.
- Search from the S3 frontend URL, not only from curl.
- Confirm the frontend displays actual image thumbnails.
- Save screenshots of upload, search results, S3 frontend URL, API Gateway methods, Lambda functions, and CloudFormation stack outputs.
