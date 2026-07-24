import asyncio
from pathlib import Path

import edge_tts


class EdgeTTSProvider:
    def __init__(self, voice: str = "hi-IN-SwaraNeural"):
        self.voice = voice

    async def _generate_async(self, text: str, output_path: Path, rate: str = "+40%"):
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=rate,          # <-- NEW
        )
        await communicate.save(str(output_path))

    def generate(
        self,
        text: str,
        output_path: Path,
        rate: str = "+40%",
    ):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        asyncio.run(
            self._generate_async(
                text=text,
                output_path=output_path,
                rate=rate,
            )
        )