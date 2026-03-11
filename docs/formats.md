# Supported Formats

This documents the audio and image formats that LoraCamp supports as *input* files within your model folders.

## Audio Formats (Samples)

LoraCamp uses FFmpeg to process audio samples. Any format supported by your FFmpeg installation should work, but we specifically test for:

- **WAV**
- **FLAC**
- **MP3**
- **OGG/Opus**

All audio samples are transcoded to **MP3 VBR 0** for optimized web streaming.

## Image Formats (Previews)

Previews (formerly covers) are processed using the Pillow library.

- **JPG / JPEG**
- **PNG**
- **WebP**

All previews are automatically resized (max 800px) and optimized as `preview.jpg`.

---

