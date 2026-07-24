import json

from app.models.segment import Segment
from app.utils.hash_utils import transcript_hash


def load_segments(path: str):
    """
    Load transcript JSON and return:
    - source language
    - list of Segment objects
    """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    source_language = data.get("source_language", data.get("language"))

    segments = []

    for item in data["segments"]:
        segments.append(
            Segment(
                start=item["start"],
                end=item["end"],
                original=item.get("text", item.get("original")),
                translated=item.get("translated"),
            )
        )

    return source_language, segments


def save_segments(
    path: str,
    source_language: str,
    target_language: str,
    segments: list[Segment],
):
    """
    Save translated transcript.
    """

    output = {
        "source_language": source_language,
        "target_language": target_language,
        "transcript_hash": transcript_hash(segments),
        "segments": [],
    }

    for segment in segments:
        output["segments"].append(
            {
                "start": segment.start,
                "end": segment.end,
                "original": segment.original,
                "translated": segment.translated,
            }
        )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)