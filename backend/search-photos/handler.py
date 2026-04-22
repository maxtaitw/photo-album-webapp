import json


def lambda_handler(event, context):
    query_string_parameters = event.get("queryStringParameters") or {}
    query = query_string_parameters.get("q", "")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(
            {
                "query": query,
                "results": [],
            }
        ),
    }
