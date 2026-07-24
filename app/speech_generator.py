from pathlib import Path
import subprocess
import time

from app.edge_tts_provider import EdgeTTSProvider
from app.models.segment import Segment
from app.utils import load_segments
import wave



class SpeechGenerator:
    """
    Generates speech audio for translated transcript segments.
    """

    def _get_wav_duration(self, wav_path: Path) -> float:
        with wave.open(str(wav_path), "rb") as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            return frames / rate


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

        for index, segment in enumerate(segments):
            original_duration = segment.end - segment.start

            self._generate_segment(
                index=index,
                segment=segment,
                original_duration=original_duration,
            )

            print(f"[{index + 1}/{total}] Done")

        print("\nSpeech generation completed!")

    def _generate_segment(
        self,
        index: int,
        segment: Segment,
        original_duration: float,
    ):
        wav_file = self.output_dir / f"segment_{index:04d}.wav"
        mp3_file = self.output_dir / f"segment_{index:04d}.mp3"

        # Resume support
        if wav_file.exists():
            return

        MAX_ALIGNMENT_ATTEMPTS = 3
        TOLERANCE = 0.10

        rate = "+40%"

        for attempt in range(MAX_ALIGNMENT_ATTEMPTS):

            # ---------- Generate ----------
            self.provider.generate(
                text=segment.translated,
                output_path=mp3_file,
                rate=rate,
            )

            self._convert_to_wav(mp3_file, wav_file)

            generated_duration = self._get_wav_duration(wav_file)

            diff = abs(generated_duration - original_duration)

            print(
                f"Attempt {attempt + 1} | "
                f"Target={original_duration:.2f}s | "
                f"Generated={generated_duration:.2f}s | "
                f"Rate={rate}"
            )

            if diff <= original_duration * TOLERANCE:
                break

            rate = self._calculate_rate(
                original_duration,
                generated_duration,
            )

            if mp3_file.exists():
                mp3_file.unlink()

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

    def _calculate_rate(
        self,
        original_duration: float,
        generated_duration: float,
    ) -> str:
        """
        Calculate the Edge-TTS speaking rate needed to bring the
        generated duration closer to the original duration.
        """

        if original_duration <= 0:
            return "+40%"

        ratio = generated_duration / original_duration

        # Convert ratio into a percentage adjustment.
        # ratio > 1 => generated speech is too long -> speak faster.
        percent = round((ratio - 1.0) * 100)

        # Edge-TTS works best in this range.
        percent = max(-50, min(80, percent))

        if percent >= 0:
            return f"+{percent}%"

        return f"{percent}%"