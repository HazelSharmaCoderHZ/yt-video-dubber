from pathlib import Path
import yt_dlp

from app.config import TEMP_DIR
from app.logger import logger


class VideoDownloader:
    def __init__(self):
        self.output_path = TEMP_DIR / "video.%(ext)s"

    def download(self, url: str) -> Path:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": str(self.output_path),
            "quiet": True,
            "noplaylist": True,
            "overwrites": True,
        }

        logger.info("Downloading video...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return Path(filename)