# LoraCamp Metadata JSON Reference

When building a model page, LoraCamp automatically generates a metadata file structured to be compatible with tools like LoraManager
<https://github.com/willmiao/ComfyUI-Lora-Manager>

The generated metadata file is saved as `<safetensor_stem>.metadata.json` alongside the generated `.safetensors` file.

## Schema Details

Below is the format of the output JSON and how it maps to your `model.toml`.

| JSON Field | mapped from `model.toml` | Notes |
| :--- | :--- | :--- |
| `file_name` | Safetensor file stem/name (or fallback to `title`) | |
| `model_name` | `title` | |
| `size` | File size (bytes) of Safetensors | Sourced from OS |
| `modified` | Timestamp (mtime) of Safetensors | Sourced from OS |
| `sha256` | SHA256 Hash of entire Safetensors file | Computed by LoraCamp |
| `base_model` | `base_model` | Defaults to `"Other"` if undefined |
| `preview_url` | | *Currently unpopulated string* |
| `preview_nsfw_level` | | *Defaults to 0* |
| `notes` | `about` | Defaults to empty string |
| `from_civitai` | | *Defaults to false* |
| `civitai` | Object containing `trainedWords` | See below |
| `civitai.trainedWords` | `[trigger_word]` | Fallback to `[]` if no `trigger_word` |
| `tags` | | *Defaults to empty list `[]`* |
| `modelDescription` | `about` | Duplicate of `notes` for redundancy |
| `civitai_deleted` | | *Defaults to false* |
| `favorite` | | *Defaults to false* |
| `exclude` | | *Defaults to false* |
| `db_checked` | | *Defaults to false* |
| `skip_metadata_refresh` | | *Defaults to false* |
| `metadata_source` | | *Defaults to "loracamp"* |
| `last_checked_at` | | *Defaults to 0* |
| `usage_tips` | | *Defaults to "{}"* |

### Example

Suppose your safetensors file is named `MyV1.safetensors`, and your `model.toml` defines:

```toml
title = "My Cool Style"
trigger_word = "cool_style"
about = "This is a cool vintage style"
base_model = "SDXL 1.0"
```

The resulting `MyV1.metadata.json` will look like:

```json
{
  "file_name": "MyV1",
  "model_name": "My Cool Style",
  "size": 163675552,
  "modified": 1773258409.6465602,
  "sha256": "caf49b3d341e74640...",
  "base_model": "SDXL 1.0",
  "preview_url": "",
  "preview_nsfw_level": 0,
  "notes": "This is a cool vintage style",
  "from_civitai": false,
  "civitai": {
    "trainedWords": [
      "cool_style"
    ]
  },
  "tags": [],
  "modelDescription": "This is a cool vintage style",
  "civitai_deleted": false,
  "favorite": false,
  "exclude": false,
  "db_checked": false,
  "skip_metadata_refresh": false,
  "metadata_source": "loracamp",
  "last_checked_at": 0,
  "usage_tips": "{}"
}
```
