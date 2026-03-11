# Command-line Arguments

Run `python -m loracamp.main --help` for the most up-to-date information.

## Primary Arguments

- `catalog_dir`: The directory containing your models and manifests (default is current directory).
- `--build`: Triggers the site generation process.
- `--output <DIR>`: Where to save the generated site (default is `buildsite`).

## Implementation Status (CLI)

| Argument | LoraCamp Status | Description |
| :--- | :--- | :--- |
| `--build` | [x] Supported | Generates the static site. |
| `--output` | [x] Supported | Sets the destination directory. |
| `--cdn-url` | [x] Supported | Points model/sample links to a remote URL. |
| `--include/--exclude` | [ ] Todo | Filter which models to process by pattern. |
| `--debug` | [ ] Todo | Print catalog info without building. |

---
*Note: Many advanced Faircamp CLI flags are planned for future LoraCamp releases.*
