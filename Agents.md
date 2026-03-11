# AI Assistant Rules & Guidance - LoraCamp

## Project Overview
- **Name**: LoraCamp (a port of faircamp)
- **Language**: ONLY Python
- **Source**: Porting from Rust (see `referencecode/` directory)
- **License**: GNU Affero General Public License (AGPL) 3.0

## Core Principles
1. **No Dropping Functionality**: Never drop any functionality from the original `faircamp` code without explicitly asking the user.
2. **No Stub Code**: Always provide full implementation. Never use placeholders or "stub" functions.
3. **Testability**: All code should be written with testability in mind. Always provide options for testing.
4. **Python Only**: Do not introduce any other languages unless strictly necessary and approved (e.g., build scripts should still be Python if possible).

## Porting Strategy
- **Not a 1:1 Port**: While we use `faircamp` (specifically the fork in `referencecode/`) as our functional base, LoraCamp is an adaptation. 
- **Terminology Shift**: Replace "music/album" terminology with "model/sample" where appropriate in the UI and documentation. 
  > [!IMPORTANT]
  > While "Model" and "Creator" are used as domain-specific terms for manifests and data, the software brand and core engine class name remains **LoraCamp** / **LoraCampEngine**.
- **Manifest Format**: Use **TOML** for all manifest files (replacing the reference `.eno` format). This is a known standard and easy for both humans and AI to read/write.
- **Transcoding**: Use `python-ffmpegio` and `static-ffmpeg` for all media processing.
- **i18n**: Use **gettext** for runtime translations and **Babel** for message extraction and catalog management.
- **Templating**: Use **Jinja2**. It is widely recognized, has great AI support, and is easy for humans to maintain.
- **Safetensors**: Treat `.safetensors` files as "attachments" initially. 
- **Metadata Generation**: Automatically generate a metadata JSON for each safetensor. This JSON should combine user-provided info (About, TriggerWord, Author, etc.) from manifests with technical data (e.g., SHA256). This JSON will be hosted on the site and bundled with downloads.
- **Build Directories**: Do NOT use hidden dot-files (like `.faircamp_build`). Instead, use visible, user-friendly directories such as `/yoursite` for the static website and `/yourcdn` for CDN-hosted content. This makes it easier for users to browse, copy, or FTP their files.
## New Functionality
- **CDN Splitting**: Support splitting the build into a "static site" and "CDN content".
- **Metadata Bundling**: Ensure that every shared Lora includes its machine-readable metadata in a standard JSON format, making the site easy to scrape and the models easy to identify.

## Environment
- Use a virtual environment (managed by `uv` or `venv`) for all dependencies.
- Dependencies should be managed via modern Python tools, primarily **uv** (preferred) or standard `pip` with `requirements.txt`/`pyproject.toml`.
