import json

from lex_client import interpret_query
from search_client import search_photos


def lambda_handler(event, context):
    query_string_parameters = event.get("queryStringParameters") or {}
    query = query_string_parameters.get("q", "")
    keywords = interpret_query(query)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(
            {
                "query": query,
                "keywords": keywords,
                "results": search_photos(keywords),
            }
        ),
    }
