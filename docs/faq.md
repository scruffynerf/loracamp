# Frequently Asked Questions

## Why does LoraCamp transcode my audio files?

When you build your catalog, LoraCamp automatically transcodes your source audio files (like WAV or FLAC) into optimized formats (currently **Opus** at 96kbps VBR).

The reasons for this are:

1. **Modern Web Efficiency**: Opus provides superior audio quality at lower bitrates compared to MP3 or AAC, ensuring fast loading times for your visitors.
2. **Loudness Normalization**: LoraCamp applies EBU R128 loudness normalization (targeted at -16 LUFS) so all samples across your catalog have a consistent volume level.
3. **Metadata Cleaning**: During transcoding, LoraCamp strips all existing metadata and injects a clean set of tags (Title and Artist) directly into the Opus files.

## How are Safetensors handled?

`.safetensors` files are treated as primary model assets. LoraCamp calculates a SHA256 hash for each model and bundles it into a `metadata.json` file. This allows for easy verification and scraping by external tools.

## Can I use images instead of audio for samples?

Currently, LoraCamp focuses on audio samples, but we plan to support image-based samples and workflows in future updates. Keep an eye on our [roadmap](../porting_log.md).
