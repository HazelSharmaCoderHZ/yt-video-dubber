from pathlib import Path
from app.downloader import VideoDownloader
from app.extractor import AudioExtractor
from app.transcriber import Transcriber
from app.translator import Translator
from app.edge_tts_provider import EdgeTTSProvider
from app.speech_generator import SpeechGenerator

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

    # Phase 3 - Transcription
    print("\nTranscribing audio...")

    transcriber = Transcriber()
    transcript_path = transcriber.transcribe(audio_path)

    print("\nTranscript generated successfully!")
    print(f"Saved at: {transcript_path}")

    # Phase 4 - Translation
    print("\nTranslating transcript...")

    translator = Translator()

    translated_path = translator.translate(
        transcript_path=transcript_path,
        output_path="temp/translated_transcript.json",
        target_language="hi",
    )

    print("\nTranslation completed!")
    print(f"Saved at: {translated_path}")

    provider = EdgeTTSProvider()

    generator = SpeechGenerator(
        provider=provider,
        output_dir=Path("temp/audio_segments"),
    )

    generator.generate(
        Path("temp/translated_transcript.json")
    )


if __name__ == "__main__":
    main()