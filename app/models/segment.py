from dataclasses import dataclass
from pathlib import Path


@dataclass
class Segment:
    start: float
    end: float
    original: str
    translated: str | None = None
    audio_path: Path | None = None