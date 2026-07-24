import asyncio
from pathlib import Path

import edge_tts


class EdgeTTSProvider:
    """
    Handles speech synthesis using Microsoft Edge TTS.
    """

    def __init__(self, voice: str = "hi-IN-SwaraNeural"):
        self.voice = voice

    async def _generate_async(self, text: str, output_path: Path):
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(str(output_path))

    def generate(self, text: str, output_path: Path):
        """
        Generate speech for the given text.

        Parameters
        ----------
        text : str
            Text to synthesize.
        output_path : Path
            Path where the audio file will be saved.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        asyncio.run(self._generate_async(text, output_path))