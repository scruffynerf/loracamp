# LoraCamp Code Changes

This file records significant code changes, implementations, and porting milestones.

## Phase 1: Engine Foundation & Porting (2026-03-11)

### Infrastructure & CLI
- **Entry Point**: Created `loracamp/main.py` with `argparse` for a robust CLI.
- **Build Engine**: Implemented `loracamp/engine.py` to orchestrate scanning, manifest parsing, and site generation.
- **Visible Build Paths**: Configured the engine to output to `/yoursite` and `/yourcdn` instead of hidden dot-files.
- **Dependency Management**: Initialized `pyproject.toml` and `requirements.txt` with `tomli`, `jinja2`, `babel`, and `python-ffmpeg`.

### Manifests & Logic
- **TOML Implementation**: Created `loracamp/manifests.py`. Replaced Faircamp's `.eno` format with TOML for better Python ecosystem integration.
- **Metadata Engine**: Created `loracamp/metadata.py`. Implemented SHA256 hashing for `.safetensors` files and automated `metadata.json` assembly.
- **CDN Strategy**: Created `loracamp/cdn.py`. Implemented logic to separate large binary files from static site assets.

### Frontend & Assets
- **Templates**: Set up Jinja2 environment in `loracamp/templates/`.
    - Created `base.html` for layout.
    - Created `index.html` for the catalog view.
- **CSS Port**: Migrated the reference minimalist `site.css` into `loracamp/static/css/`.
- **Localization**: Created `loracamp/i18n.py` using standard Python `gettext` patterns.

## Phase 2: Media & Metadata Enhancement (2026-03-11)

### Media Processing
- **Audio Transcoding**: Implemented `loracamp/media.py` using `python-ffmpegio` for a cleaner API, removing raw `subprocess` overhead while still leveraging `static-ffmpeg` for zero-config binaries.
- **Duration Extraction**: Added `ffprobe` integration to extract audio duration for the player.
- **Image Optimization**: Integrated `Pillow` to automatically resize and optimize Lora previews to `preview.jpg`.

### Site Structure & Features
- **Lora Detail Pages**: Implemented `lora.html` template and engine logic to generate individual model pages.
- **Slug-Based CDN**: Refined the CDN strategy to mirror the site's slug structure (`/yourcdn/SLUG/` matches `/yoursite/SLUG/`).
- **Sample Discovery**: Automated the scanning of model folders for audio assets and linking them to the site.
- **Manifest Gap Analysis**: Conducted a comprehensive audit of all Faircamp manifest types (`artist`, `catalog`, `release`, `track`) identifying over 20 unported features (distribution, commerce, social, and anti-hotlinking) and documented them in `porting_log.md` and the internal reference guides.

### Software Identity & Branding
- **LoraCamp Branding**: Reverted core engine class to `LoraCampEngine` to preserve the software's brand identity while maintaining "Model" and "Creator" as domain-specific terminology for manifests and data.
- **Rules Disclosure**: Updated `AGENTS.md` with explicit guidelines on this distinction.

### Dependencies
- Added `Pillow` for image processing.
- Added `python-ffmpegio` for higher-level media control.
- Added `static-ffmpeg` for bundled binaries.
