PHOTO_DATASET = [
    {
        "objectKey": "sample-photo.jpg",
        "bucket": "photo-album-storage-bucket",
        "createdTimestamp": "2026-04-22T12:40:02.000Z",
        "labels": ["dog", "park", "sam", "sally"],
    },
    {
        "objectKey": "forest-birds.jpg",
        "bucket": "photo-album-storage-bucket",
        "createdTimestamp": "2026-04-23T09:15:00.000Z",
        "labels": ["trees", "birds", "forest"],
    },
]


def search_photos(keywords):
    if not keywords:
        return []

    results = []
    for photo in PHOTO_DATASET:
        photo_labels = set(photo["labels"])
        if any(keyword in photo_labels for keyword in keywords):
            results.append(photo)

    return results
