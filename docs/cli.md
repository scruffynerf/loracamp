# Command-line Arguments

Run `uv run loracamp --help` for the most up-to-date information.

## Primary Arguments

- `catalog`: The directory containing your models and manifests (default is current directory).
- `--build`: Triggers the site generation process.
- `--output <DIR>`: Where to save the generated site (default is current directory `.`).
- `--cdn-url <URL>`: Points model and sample links to a remote storage provider instead of relative local paths.
- `--include <PATTERN>`: Only process paths containing this pattern. Can be used multiple times.
- `--exclude <PATTERN>`: Skip paths containing this pattern. Can be used multiple times.
- `--preview`: Start a local webserver to view the generated site.
- `--port <PORT>`: Set the port for the preview server (default: 8000).

## Implementation Status (CLI)

| Argument | LoraCamp Status | Description |
| :--- | :--- | :--- |
| `--build` | [x] Supported | Generates the static site. |
| `--output` | [x] Supported | Sets the destination directory. |
| `--cdn-url` | [x] Supported | Points model/sample links to a remote URL. |
| `--include/--exclude` | [x] Supported | Filter which models to process by pattern. |
| `--preview` | [x] Supported | Locally preview the build in a webserver. |
| `--port` | [x] Supported | Customize the port for the preview server. |
| `--deploy` | [ ] Todo | Deploy via rsync (Faircamp `-d`). |
| `--debug` | [ ] Todo | Print catalog diagnostics without building. |
| `--theming-widget` | [ ] Todo | Inject an interactive theme editor into the build. |
| `--no-clean-urls` | [ ] Todo | Generate links with `index.html` for local browsing. |

---

## Faircamp Parity Gaps

Several advanced Faircamp CLI features are not yet implemented in LoraCamp:

### Cache Optimization

Faircamp tracks asset hashes to skip re-transcoding and provides:

- `--analyze-cache`: See how much space is used by obsolete assets.
- `--optimize-cache`: Reclaim disk space.
- `--wipe-cache`: Delete all cached assets.

### Deploy & Preview

- `--deploy`: LoraCamp currently assumes manual upload/FTP. Faircamp automates this via `rsync`.

### Maintenance

- `--wipe-all` / `--wipe-build`: Quickly clear out your site or build directories.

---
*Note: This reference tracks CLI parity with the original Faircamp implementation.*
