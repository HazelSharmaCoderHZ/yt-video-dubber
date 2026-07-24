"# yt-video-dubber" 
# 🎬 Automated Video Dubbing System

An AI-powered Python application that automatically dubs YouTube videos into another language using speech recognition, machine translation, and text-to-speech synthesis.

---

## ✨ Features

- 📥 Download YouTube videos
- 🎵 Extract audio using FFmpeg
- 📝 Transcribe speech with Faster-Whisper
- 🌐 Translate transcripts using Google Gemini
- 🗣️ Generate natural speech using Microsoft Edge-TTS
- 🎯 Align generated audio with original timestamps
- 🎥 Merge dubbed audio with the original video

---

## 🛠️ Tech Stack

- Python
- yt-dlp
- FFmpeg
- Faster-Whisper
- Google Gemini API
- Edge-TTS
- NumPy

---

## 📂 Project Structure

```
app/
├── downloader.py
├── audio_extractor.py
├── transcriber.py
├── translator.py
├── speech_generator.py
├── audio_aligner.py
├── gemini_translator.py
├── edge_tts_provider.py
└── utils/

main.py
```

---

## 🚀 Pipeline

```
YouTube Video
      │
      ▼
Video Download
      │
      ▼
Audio Extraction
      │
      ▼
Speech-to-Text (Whisper)
      │
      ▼
Translation (Gemini)
      │
      ▼
Speech Generation (Edge-TTS)
      │
      ▼
Audio Alignment
      │
      ▼
Video + Audio Merge
      │
      ▼
Dubbed Video
```

---

## ⚙️ Installation

```bash
git clone <repository-url>
cd dubber

pip install -r requirements.txt
```

Install **FFmpeg** and add it to your system PATH.

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Usage

```bash
python main.py
```

Enter the YouTube URL when prompted.

The final dubbed video will be generated as:

```
output_dubbed.mp4
```

---

## 📌 Future Improvements

- Multi-language dubbing
- Voice cloning
- Lip synchronization
- Background music preservation
- Speaker diarization
- Emotion-aware speech synthesis

---

## 👨‍💻 Author

**Hazel Sharma**

B.Tech Information Technology, VIT Vellore