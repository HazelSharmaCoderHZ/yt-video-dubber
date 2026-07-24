from pathlib import Path
import subprocess
import time

from app.edge_tts_provider import EdgeTTSProvider
from app.models.segment import Segment
from app.utils import load_segments


class SpeechGenerator:
    """
    Generates speech audio for translated transcript segments.
    """

    def __init__(
        self,
        provider: EdgeTTSProvider,
        output_dir: Path,
    ):
        self.provider = provider
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, transcript_path: Path):
        _, segments = load_segments(transcript_path)

        total = len(segments)

        print(f"\nGenerating speech for {total} segments...\n")

        for index, segment in enumerate(segments, start=1):
            self._generate_segment(index, segment)
            print(f"[{index}/{total}] Done")

        print("\nSpeech generation completed!")

    def _generate_segment(self, index: int, segment: Segment):
        wav_file = self.output_dir / f"segment_{index:04d}.wav"

        # Resume support
        if wav_file.exists():
            return

        mp3_file = self.output_dir / f"segment_{index:04d}.mp3"

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):
            try:
                self.provider.generate(
                    text=segment.translated,
                    output_path=mp3_file,
                )
                break

            except Exception:
                if attempt == MAX_RETRIES - 1:
                    raise

                wait = 2 ** attempt
                print(f"Retrying segment {index} in {wait} seconds...")
                time.sleep(wait)

        self._convert_to_wav(mp3_file, wav_file)

        if mp3_file.exists():
            mp3_file.unlink()

    def _convert_to_wav(self, mp3_path: Path, wav_path: Path):
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(mp3_path),
            "-ac",
            "1",
            "-ar",
            "16000",
            "-acodec",
            "pcm_s16le",
            str(wav_path),
        ]

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )