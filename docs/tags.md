# Metadata and Tags

LoraCamp handles two types of metadata: **Audio Sample Metadata** (embedded in files) and **Classification Tags** (used for organization and discovery on the site).

## Audio Sample Metadata

When LoraCamp transcodes your audio samples, it applies a broad "normalization" to ensure compatibility and consistency.

### Transcoding Details

- **Format**: Opus (inside an Ogg container).
- **Quality**: 96kbps VBR (Variable Bitrate).
- **Normalization**: EBU R128 loudness normalization (targeted at -16 LUFS).

### Embedded Tags

During transcoding, LoraCamp strips all existing metadata and adds back:

- **Title**: Derived from the sample's `title` (in `sample.toml`) or the filename.
- **Artist**: Derived from the Model's `author` or the Catalog's `creator`.

> [!NOTE]
> We currently convert to **Opus** for small file size and good quality.

## Classification Tags

You can add classification tags to your **models** in `model.toml` and to individual **samples** in `sample.toml`. These tags are used to organize your collection, improve search results, and are exported in the machine-readable metadata.

### Usage in `model.toml` / `sample.toml`

Add a `tags` list to your manifest:

```toml
tags = ["photorealistic", "vintage", "portrait", "indoor"]
```

Sample-specific tags allow users to find specific demos (e.g., a "Jazz" tag for a specific sample even if the Model itself is more general).

### Export to JSON

These tags are automatically included in the `<safetensor_stem>.metadata.json` file generated during the build. This ensures that browsers, scrapers, and local model managers (like LoraManager) can correctly categorize your models.

## Future Plans

- **Tag-based Filtering**: Automatic generation of tag indices on the homepage for easy browsing.
- **Audio Tag Control**: Options like `tags = "copy"` or `tags = "remove"` to control sample metadata behavior.
