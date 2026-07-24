from pathlib import Path

from app.edge_tts_provider import EdgeTTSProvider

provider = EdgeTTSProvider()

provider.generate(
    text="नमस्ते! यह हमारी पहली डबिंग है।",
    output_path=Path("temp/test.wav"),
)

print("Speech generated successfully!")