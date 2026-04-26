# Photo Album Web App

Cloud Computing and Big Data Systems - Spring 2026, Assignment 3.

This project will implement a searchable photo album web application using AWS services. Users will be able to upload photos, attach optional custom labels, search with natural language text, and view matching photo results.

## Assignment Goal

Build a photo search application backed by:

- Amazon S3 for photo storage and static frontend hosting
- AWS Lambda for indexing and searching
- Amazon Rekognition for automatic image labels
- Amazon OpenSearch Service or Elasticsearch for searchable metadata
- Amazon Lex for extracting search keywords
- Amazon API Gateway for upload and search endpoints
- AWS CodePipeline for deployment
- AWS CloudFormation for basic infrastructure provisioning

## Expected API

- `PUT /photos`
- `GET /search?q={query text}`

## Required Lambda Functions

- `index-photos`: triggered by S3 photo uploads, detects labels, reads custom metadata, and indexes photo metadata.
- `search-photos`: receives a query, uses Lex to extract keywords, searches the photo index, and returns matching photos.

## Required Custom Label Behavior

Photo uploads must support custom labels through this S3 metadata header:

```http
x-amz-meta-customLabels: label one, label two
```

Custom labels must be searchable the same way Rekognition labels are searchable.

## Plan

- [x] Set up the repository and baseline documentation.
- [x] Create the project folder structure.
- [x] Create the backend Lambda structure.
- [x] Implement photo indexing locally as much as possible before AWS deployment.
- [x] Add search behavior.
- [x] Build the API layer.
- [ ] Build the frontend.
- [ ] Add deployment resources.
- [ ] Add the basic CloudFormation template.

## Repository Structure

- `backend/`: Lambda functions and backend configuration.
- `frontend/`: Static web application files.
- `infrastructure/`: CloudFormation, deployment notes, and AWS setup notes.

## Team Handoff

For the current deployed backend state and teammate instructions, see `infrastructure/team-handoff.md`.
