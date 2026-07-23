from pathlib import Path
import subprocess

from app.logger import logger


class AudioExtractor:
    def extract(self, video_path: Path) -> Path:
        output_path = video_path.with_suffix(".wav")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(output_path),
        ]

        logger.info("Extracting audio...")

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        logger.info("Audio extracted successfully.")

        return output_path