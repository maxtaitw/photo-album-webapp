# index-photos Lambda

`index-photos` is triggered when a new photo is uploaded to the photo storage S3 bucket.

## Event Input

This function receives an S3 `ObjectCreated:Put` event.

Important fields:

- S3 bucket name
- S3 object key
- Object creation time from the event or object metadata

## Responsibilities

1. Read the uploaded photo location from the S3 event.
2. Call Amazon Rekognition `DetectLabels` for the image.
3. Read optional upload metadata using S3 `HeadObject`.
4. Extract custom labels from:

```http
x-amz-meta-customLabels
```

5. Combine Rekognition labels and custom labels into one searchable labels list.
6. Store a photo metadata document in the `photos` OpenSearch index.

## Indexed Document Shape

```json
{
  "objectKey": "my-photo.jpg",
  "bucket": "my-photo-bucket",
  "createdTimestamp": "2018-11-05T12:40:02",
  "labels": ["person", "dog", "ball", "park"]
}
```

## Required AWS Permissions

The Lambda execution role will need permission to:

- Read the uploaded S3 object metadata with `s3:HeadObject`.
- Pass the S3 object to Rekognition with `rekognition:DetectLabels`.
- Write indexed documents to OpenSearch.
- Write logs to CloudWatch Logs.

## First Test

Upload one image to the photo bucket and confirm:

- The Lambda is invoked.
- Rekognition labels are visible in CloudWatch logs.
- Custom labels are read when the upload includes `x-amz-meta-customLabels`.
- A document is created in the `photos` index.

## Local Sample Event

Use `events/s3-put.json` to understand the S3 event shape before deploying to AWS.
