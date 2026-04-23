import re


FILLER_WORDS = {
    "show",
    "me",
    "photo",
    "photos",
    "with",
    "and",
    "in",
    "them",
}


def normalize_query(text):
    if not text:
        return ""

    return str(text).strip().lower()


def extract_keywords(text):
    normalized = normalize_query(text)
    if not normalized:
        return []

    words = re.findall(r"[a-z0-9]+", normalized)

    keywords = []
    seen = set()
    for word in words:
        if word in FILLER_WORDS or word in seen:
            continue

        seen.add(word)
        keywords.append(word)

        if len(keywords) == 2:
            break

    return keywords
