# Frequently Asked Questions

## Why does LoraCamp transcode my audio files?

When you build your catalog, LoraCamp automatically transcodes your source audio files (like WAV or FLAC) into optimized formats (currently MP3).

The reasons for this are:
1.  **Web Compatibility**: Not all browsers support every audio format natively. MP3 is a universal standard.
2.  **Streaming Efficiency**: We transcode to a bitrate optimized for web streaming to ensure fast loading times and reduced bandwidth usage for your visitors.
3.  **Metadata Bundling**: During the transcoding process, LoraCamp can inject metadata (like the Model title and Creator name) directly into the audio files.

## How are Safetensors handled?

`.safetensors` files are treated as primary model assets. LoraCamp calculates a SHA256 hash for each model and bundles it into a `metadata.json` file. This allows for easy verification and scraping by external tools.

## Can I use images instead of audio for samples?

Currently, LoraCamp focuses on audio samples, but we plan to support image-based samples and workflows in future updates. Keep an eye on our [roadmap](../porting_log.md).
