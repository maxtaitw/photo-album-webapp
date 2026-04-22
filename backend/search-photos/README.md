# search-photos Lambda

`search-photos` handles photo search requests from API Gateway.

## Event Input

This function receives a request from:

```http
GET /search?q={query text}
```

Important fields:

- Query string parameter `q`

## Responsibilities

1. Read the query text from the API Gateway request.
2. Send the query text to Amazon Lex.
3. Extract one or two search keywords from the `SearchIntent` result.
4. Search the `photos` OpenSearch index for matching labels.
5. Return matching photo results using the assignment API response format.

## Search Behavior

Supported query examples:

- `trees`
- `birds`
- `show me trees`
- `show me photos with trees and birds in them`

If Lex does not return usable keywords, the function should return an empty result list.

## Required AWS Permissions

The Lambda execution role will need permission to:

- Call the Lex bot runtime.
- Query the OpenSearch `photos` index.
- Write logs to CloudWatch Logs.

## First Test

Call the API with a known label and confirm:

- The Lambda receives the query string.
- Lex extracts the expected keyword or keywords.
- OpenSearch returns matching indexed photos.
- The API response can be consumed by the frontend.

## Local Sample Event

Use `events/api-gateway-search.json` to understand the API Gateway event shape before deploying to AWS.
