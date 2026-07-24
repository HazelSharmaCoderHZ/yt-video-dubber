import json
from pathlib import Path

from app.tts import TTSGenerator


class SpeechGenerator:
    def __init__(self):
        self.tts = TTSGenerator()

    def generate(
        self,
        transcript_path: str,
        output_dir: str,
    ):
        transcript_path = Path(transcript_path)
        output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        generated_files = []

        for index, segment in enumerate(transcript["segments"]):
            filename = f"{index:03}.mp3"
            output_path = output_dir / filename

            print(f"Generating {filename}...")

            self.tts.generate(
                segment["translated"],
                output_path,
            )

            generated_files.append(output_path)

        print("\nSpeech generation completed.")

        return generated_files