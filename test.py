from pathlib import Path

from app.transcriber import Transcriber

transcriber = Transcriber()

result = transcriber.transcribe(
    Path("temp/video.wav")
)

print(result)