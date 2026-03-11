# catalog.toml Reference

The `catalog.toml` file at the root of your directory controls global site settings.

## Options

### `title`
The title of your Lora collection.
```toml
title = "My Awesome Loras"
```

### `author`
The default author name for the collection.
```toml
author = "Artisan"
```

### `base_url`
The URL where your site will be hosted. Required for generating absolute links in metadata.
```toml
base_url = "https://loracamp.example.com"
```

### `cdn_url` (Optional)
The URL of your external storage provider if you are hosting large files separately.
```toml
cdn_url = "https://cdn.example.com"
```

### `language` (Optional)
The language code for the site (default is `en`).
```toml
language = "en"
```

### `synopsis` (Optional)
A short, plain-text introduction for your catalog homepage (max 256 chars).
```toml
synopsis = "A collection of high-quality Stable Diffusion Loras for photographers."
```

### `about` (Optional)
Long-form content for the homepage (supports Markdown). Usually appears after the model list.
```toml
about = """
## Welcome to my Lora collection
All models here are trained on custom datasets...
"""
```

### `links` (Optional)
A list of external links to show in the header.
```toml
[[links]]
label = "Twitter"
url = "https://twitter.com/myaccount"

[[links]]
label = "HuggingFace"
url = "https://huggingface.co/myuser"
```

### `theme` (Optional)
Customize the visual appearance.
```toml
[theme]
base = "dark" # "light" or "dark"
accent_hue = 210 # 0-360
accent_chroma = 80 # 0-100
round_corners = true
```

### `site_assets` & `site_metadata` (Advanced)
Include custom CSS/JS in the build and the `<head>` section.
```toml
site_assets = ["custom.css", "analytics.js"]

site_metadata = """
<link rel="stylesheet" href="{{custom.css}}">
<script src="{{analytics.js}}"></script>
"""
```

---

## Pending Implementation (Faircamp Gaps)

The following features from Faircamp's `catalog.eno` are not yet implemented in LoraCamp:

| Field | Description |
| :--- | :--- |
| `feeds` | Generation of RSS/Atom/Podcast feeds. |
| `opengraph` | Support for Open Graph social metadata tags. |
| `cache_optimization` | Advanced control over asset purging (`delayed`, `immediate`, `wipe`). |
| `rotate_download_urls` | Logic for randomizing download URLs on every build. |
| `freeze_download_urls` | Manual randomization of download URLs for anti-hotlinking. |
| `label_mode` | Multi-artist support where the homepage shows a roster instead of a single creator. |
| `faircamp_signature` | Toggle to disable the LoraCamp footer credits. |
| `feature_support_artists`| Logic for linking guest creators to their own pages. |

---
*Note: This is an evolving reference based on Faircamp's feature set.*
