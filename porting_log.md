# LoraCamp Porting Log

This log tracks functionality from the reference `faircamp` implementation and its status in the `loracamp` port.

## Documentation & Non-Code Assets

| Item | Reference Path | Status | Notes |
| :--- | :--- | :--- | :--- |
| Manual | `manual/` | [x] Ported | All 10 topics and 4 reference pages ported and adapted. |
| CSS Assets | `src/assets/` | [x] Ported | Referenced `site.css` ported; aesthetics improvement is a future goal. |
| JS Assets | `src/assets/` | [ ] Pending | Focus on audio Samples (MP3s) first. |
| HTML Templates | `src/render/` | [x] Ported | Jinja2 templates (`base.html`, `index.html`) renamed and updated. |
| Manifests | `N/A` | [x] Implemented | Using **TOML**; Model/Creator models and parsing logic in `manifests.py`. |
| Translations | `translations/src/` | [/] In Progress | Standard Python i18n established; initial `en.json` created. |
| **All Manifests**| `manual/reference/` | [/] In Progress | Core fields ported to TOML; many niche/distribution fields pending (see below). |

## Core Functionality

| Functionality | Status | Adaptation Strategy |
| :--- | :--- | :--- |
| Static Site Generation | [x] Implemented | Python engine (`engine.py`) and Jinja2. |
| Media Transcoding | [x] Implemented | Integrated `static-ffmpeg` for zero-config transcoding. |
| "Live Site" Preview | [X] Dropped | Dropped as requested. |
| Audio/Image Metadata | [ ] Pending | Extract from MP3s and Safetensors. |
| Folder-as-Model      | [x] Implemented | `ModelCampEngine` handles model discovery and processing. |
| **CDN Splitting** (NEW) | [x] Implemented | Logic in `cdn.py` handles `/yoursite` and `/yourcdn` paths. |
| **Metadata Generation** (NEW)| [x] Implemented | `metadata.py` handles SHA256 and JSON assembly. |
| Path Filtering       | [ ] Pending | Port `--include` and `--exclude` logic (Topic 05). |
| Local Browsability   | [x] Implemented | Explicit `index.html` URLs are now the default. |
| Image/Audio Formats  | [x] Implemented | Python wrapper for FFmpeg and Pillow (Topic 06). |
| Granular Tagging     | [ ] Pending | Port `tags: copy/remove/rewrite` logic (Topic 09). |
| Multi-format Stream  | [ ] Pending | Port Opus+MP3 fallback for streaming (Topic 10). |
| Creator/Model Aliases| [ ] Pending | Port name matching with aliases (Artist Ref). |
| External Linking     | [ ] Pending | Port `external_page` to redirect creator/model (Artist Ref). |
| Download Codes       | [ ] Pending | Port `download_code(s)` and `unlock_info` (Sample Ref). |
| Embedding Widgets    | [ ] Pending | Port `embedding: enabled` for IFrame support (Sample Ref). |

## Manifest Feature Gaps (Unported from Faircamp)

| Feature Area | Missing Fields / Logic | Notes |
| :--- | :--- | :--- |
| **Catalog** | `feeds`, `opengraph`, `label_mode`, `cache_optimization`, `rotate_download_urls` | RSS/Atom feeds and social metadata are high-priority gaps. |
| **Creator** | `aliases`, `rel="me"` links, `external_page`, `m3u` | Alias matching is critical for messy ID3 tags. |
| **Model**   | `release_downloads`, `release_extras`, `release_price`, `paycurtain` | Multi-format ZIP bundling and commerce features are pending. |
| **Sample**  | `track_downloads`, `track_extras`, `cover` (per-sample) | Individual file downloads and per-sample art logic. |
| **Player/UI** | `speed_controls`, `streaming_quality`, `waveforms: absolute/disabled`, `copy_link` | Granular UI/UX toggles from the original player. |
| **Processing**| `tags: copy/remove/rewrite`, `normalize` | Fine-grained ID3 tag management. |

## Items of Interest / Flags
- **[FLAG]** Safetensors-as-attachments: Port reference "attachments" logic to handle `.safetensors`.
- **[FLAG]** Jinja2 is the chosen templating engine for its ease of use and standard status.
- **[FLAG]** TOML is the chosen manifest format.
