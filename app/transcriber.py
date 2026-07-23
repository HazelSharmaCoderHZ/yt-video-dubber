from pathlib import Path
import json

from faster_whisper import WhisperModel


class Transcriber:
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_path: Path) -> Path:
        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5,
            vad_filter=True,
        )

        transcript = []
        print(f"Detected language: {info.language}")
        print(f"Confidence: {info.language_probability:.2f}")
        for segment in segments:
            transcript.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )

        output_path = audio_path.parent / "transcript.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=4, ensure_ascii=False)

        return output_path