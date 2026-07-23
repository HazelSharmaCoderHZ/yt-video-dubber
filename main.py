from app.downloader import VideoDownloader
from app.extractor import AudioExtractor


def main():
    print("=" * 50)
    print(" Automated Video Dubbing System ")
    print("=" * 50)

    url = input("\nEnter YouTube URL:\n> ").strip()

    # Phase 1 - Download
    print("\nDownloading video...")

    downloader = VideoDownloader()
    video_path = downloader.download(url)

    print("\nVideo downloaded successfully!")
    print(f"Saved at: {video_path}")

    # Phase 2 - Audio Extraction
    print("\nExtracting audio...")

    extractor = AudioExtractor()
    audio_path = extractor.extract(video_path)

    print("\nAudio extracted successfully!")
    print(f"Saved at: {audio_path}")


if __name__ == "__main__":
    main()