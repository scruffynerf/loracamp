# Audio Tags

This documents how LoraCamp handles metadata (tags) in your audio samples.

## Automated Tagging

By default, LoraCamp "normalizes" your audio tags during transcoding. It strips existing metadata and adds back:

- **Title**: Derived from the filename or `lora.toml`.
- **Artist**: Derived from the `author` field in `lora.toml` or `catalog.toml`.
- **Album**: Set to the Lora's title.

## Supported Formats

While LoraCamp can read tags from many formats (FLAC, WAV, MP3), it currently outputs **MP3** files. These use **ID3v2.3** for maximum compatibility with legacy players and operating systems.

## Future Plans

We plan to support more granular control over tags (similar to Faircamp's `tags: copy` or `tags: remove` options) in future releases.

---

