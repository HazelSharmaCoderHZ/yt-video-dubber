import json
import wave
from pathlib import Path

import numpy as np

from app.config import TEMP_DIR


class AudioAligner:
    def __init__(self):
        self.transcript_path = TEMP_DIR / "translated_transcript.json"
        self.segments_dir = TEMP_DIR / "audio_segments"
        self.output_path = TEMP_DIR / "dubbed_audio.wav"

    def _read_wav(self, path: Path):
        with wave.open(str(path), "rb") as wav:
            frames = wav.readframes(wav.getnframes())
            sample_rate = wav.getframerate()

        audio = np.frombuffer(frames, dtype=np.int16)
        return audio, sample_rate

    def analyze(self):
        with open(self.transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        sample_rate = 16000
        final_audio = np.array([], dtype=np.int16)

        current_ms = 0

        for i, seg in enumerate(transcript["segments"]):

            wav_path = self.segments_dir / f"segment_{i:04d}.wav"

            if not wav_path.exists():
                continue

            audio, sample_rate = self._read_wav(wav_path)

            target_ms = int(seg["start"] * 1000)

            if target_ms > current_ms:
                silence = np.zeros(
                    int((target_ms-current_ms)*sample_rate/1000),
                    dtype=np.int16,
                )
                final_audio = np.concatenate((final_audio, silence))
                current_ms = target_ms

            final_audio = np.concatenate((final_audio, audio))

            current_ms += len(audio)*1000//sample_rate

        with wave.open(str(self.output_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(final_audio.tobytes())

        print(f"\nSaved: {self.output_path}")

        return self.output_path