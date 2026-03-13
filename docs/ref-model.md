# model.toml Reference

Each Model directory must contain a `model.toml` file to describe it.

## Options

### `title`

The display name of the Model.

```toml
title = "Vintage Film Look"
```

### `synopsis` (Optional)

A short, plain-text introduction for the model page (max 256 chars).

### `about` (Optional)

Long-form content for the model page (supports Markdown).

### `permalink` (Optional)

The URL slug for the model page. If omitted, the directory name is used.

The creator(s) of the Model. If omitted, it falls back to the catalog's creator.

```toml
creator = "PhotographyExpert"

# OR

creators = ["Alpha", "Beta"]
```

### `base_model` (Optional)

The base model architecture this Model was trained on.

```toml
base_model = "SDXL 1.0"
```

### `trigger_word` (Optional)

The trigger keyword required to activate this Model.

```toml
trigger_word = "vfilm"
```

### `version` (Optional)

The version string for this specific release.

```toml
version = "1.0.2"
```

### `tags` (Optional)

A list of classification tags for the Model. These are used for site organization and are included in the generated metadata JSON.

```toml
tags = ["photorealistic", "vintage", "portrait"]
```

### `sample_prompts` (Optional)

A list of recommended prompts to use with this Model.

```toml
sample_prompts = [
    "vfilm style, a portraits of a robot in the rain",
    "vfilm style, cinematic landscape of a neon city"
]
```

### `preview` (Optional)

The filename of the preview image (e.g., `preview.jpg`). If omitted, LoraCamp looks for `preview.jpg` or `cover.jpg` automatically.

**Note**: The selected preview image is *not* automatically offered as a separate download link alongside your other files. If you want users to be able to download the preview image directly, you must explicitly list its filename in the `extras` array below.

### `previews` (Optional)

A list of additional preview images to show in the gallery.

```toml
previews = ["sample1.png", "sample2.png"]
```

### `release_date` (Optional)

Release date in `YYYY-MM-DD` format. Used for sorting on the homepage.

```toml
release_date = "2024-03-11"
```

### `unlisted` (Optional)

If true, the Model won't appear on the homepage but its page will still be built.

```toml
unlisted = true
```

### `preview_format` (Optional)

Override the global `preview_format` for this model (e.g. `webp`).

### `links` (Optional)

A list of external links to show on the model page.

```toml
[[links]]
label = "HuggingFace"
url = "https://huggingface.co/..."
```

### `copy_link` (Optional)

Whether to show the "Copy Link" button on the model page. Defaults to `true`.

### `extras` (Optional)

A list of additional files (e.g. PDFs, text documents, supplementary images) to explicitly offer as downloads alongside the primary model and sample audio. LoraCamp automatically discovers most extra files in the directory, but you can use this array to force inclusion.

```toml
extras = ["guide.pdf", "preview.jpg"]
```

### `opengraph` (Optional)

Provide page-specific overrides for OpenGraph tags.

```toml
[opengraph]
title = "Vintage Film LoRA"
description = "Perfect for 90s style shots."
```

---

## Pending Implementation (Faircamp Gaps)

The following features from Faircamp's `release.eno` are not yet implemented in LoraCamp:

| Field | Description |
| :--- | :--- |
| `download_access` | Support for `code`, `paycurtain`, or `external` access modes. |
| `downloads` | Specifying multiple ZIP formats (FLAC, MP3, etc.). |
| `price` / `payment` | Support for currencies and payment instruction display. |

---
*Note: This is adapted from Faircamp's release options.*
