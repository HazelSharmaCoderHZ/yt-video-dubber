from app.downloader import VideoDownloader


def main():
    print("=" * 50)
    print(" Automated Video Dubbing System ")
    print("=" * 50)

    url = input("\nEnter YouTube URL:\n> ").strip()

    print("\nDownloading video...")

    downloader = VideoDownloader()
    video_path = downloader.download(url)

    print(f"\nVideo downloaded successfully!")
    print(f"Saved at: {video_path}")


if __name__ == "__main__":
    main()