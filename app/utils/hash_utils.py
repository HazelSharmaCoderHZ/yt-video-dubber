import hashlib


def transcript_hash(segments) -> str:
    """
    Create a stable hash for a transcript based on the
    original text and timestamps.
    """

    hasher = hashlib.sha256()

    for segment in segments:
        hasher.update(
            f"{segment.start}|{segment.end}|{segment.original}".encode("utf-8")
        )

    return hasher.hexdigest()