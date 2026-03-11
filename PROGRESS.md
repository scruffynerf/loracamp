# LoraCamp Porting Progress

This file tracks the current state of the port from Faircamp (Rust) to LoraCamp (Python).

## Current Status: Phase 1 (Core Engine & Foundations)
- [x] **Project Structure**: Renamed to LoraCamp, absolute Python-only requirement.
- [x] **Manifests**: Successfully switched from `.eno` to **TOML**. Parsing models implemented.
- [x] **Metadata**: Automatic **SHA256** hash generation and `metadata.json` bundling implemented.
- [x] **CDN Split**: Logic for `/yoursite` and `/yourcdn` separation implemented.
- [x] **i18n**: Standard Python `gettext` pattern established.
- [x] **Templating**: **Jinja2** environment initialized with base layout and index.
- [x] **Assets**: Minimalist CSS ported from reference code.
- [x] **CLI**: `main.py` entry point with `--build` and `--cdn-url` support.

## Feature Roadmap

### High Priority
- [x] **FFmpeg Transcoding**: Implement audio sample processing using `python-ffmpegio`.
- [x] **Model Detail Pages**: Render individual pages for each model folder.
- [ ] **Safetensor Extractions**: Extract technical metadata from `.safetensors` headers (if possible/needed).
- [x] **Manual Porting**: Ported all 10 topics and 4 reference pages from reference manual.
  - [x] Update `porting_log.md` with comprehensive gap list
  - [x] Update `docs/ref-catalog.md`
  - [x] Update `docs/ref-creator.md`
  - [x] Update `docs/ref-model.md`
  - [x] Update `docs/ref-sample.md`
- [x] **GenAI Metadata**: Added support for advanced sample metadata (CFG, Sampler, LLM settings, Audio params).

### Medium Priority
- [ ] **Vibrant Design**: Rewrite CSS to move away from minimalist look to "premium/vibrant" aesthetic.
- [ ] **Image Lora Support**: Handle image samples and galleries (currently focusing on audio).
- [ ] **Catalog Feeds**: Port RSS/Atom feed generation logic.
- [ ] **Commerce Features**: Port `release_price`, `paycurtain`, and external purchase links.
- [ ] **Distribution Features**: Port `release_downloads` (ZIP formats) and `release_extras`.
- [ ] **Anti-Hotlinking**: Port `freeze_download_urls` and randomized path logic.

### Long Term
- [ ] **Search/Filter**: Client-side search for large catalogs.
- [ ] **Theme Customization**: TOML-based theme overrides.

## Technical Decisions
- **Language**: Python 3.10+
- **Manifest Format**: TOML
- **Media Engine**: FFmpeg (`python-ffmpegio` + `static-ffmpeg`)
- **Templates**: Jinja2
- **Localization**: Babel / gettext
- **Build Output**: `/yoursite` (HTML/CSS) and `/yourcdn` (Models/Samples)

## Dropped Functionality
- **Live Preview Server**: Dropped in favor of simple filesystem browsing of `/yoursite/index.html`.

---
*Last Updated: 2026-03-11*
