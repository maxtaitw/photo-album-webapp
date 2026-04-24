import os

from query_parser import extract_keywords, normalize_query


def _boto3_client(service_name):
    import boto3

    return boto3.client(service_name)


def _get_lex_config():
    config = {
        "botId": os.environ.get("LEX_BOT_ID"),
        "botAliasId": os.environ.get("LEX_BOT_ALIAS_ID"),
        "localeId": os.environ.get("LEX_LOCALE_ID"),
    }
    missing = [name for name, value in config.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing Lex configuration: " + ", ".join(sorted(missing))
        )
    return config


def _extract_keywords_from_slots(slots):
    keywords = []
    seen = set()

    if not isinstance(slots, dict):
        return keywords

    for slot in slots.values():
        value = None
        if isinstance(slot, dict):
            value = ((slot.get("value") or {}).get("interpretedValue")) or (
                (slot.get("value") or {}).get("originalValue")
            )

        normalized = normalize_query(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            keywords.append(normalized)

        if len(keywords) == 2:
            break

    return keywords


def interpret_query(text):
    if not text:
        return []

    config = _get_lex_config()
    client = _boto3_client("lexv2-runtime")
    response = client.recognize_text(
        botId=config["botId"],
        botAliasId=config["botAliasId"],
        localeId=config["localeId"],
        sessionId="photo-search-session",
        text=text,
    )

    slots = (((response.get("sessionState") or {}).get("intent") or {}).get("slots"))
    keywords = _extract_keywords_from_slots(slots)
    if keywords:
        return keywords

    messages = response.get("messages") or []
    for message in messages:
        content = message.get("content")
        if content:
            fallback_keywords = extract_keywords(content)
            if fallback_keywords:
                return fallback_keywords

    return []
