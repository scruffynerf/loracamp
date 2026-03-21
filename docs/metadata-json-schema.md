# metadata.json Schema Documentation

This document defines the schema for `<model>.metadata.json` sidecar files supported by LoraCamp. These files store model metadata (LoRAs, Checkpoints, Embeddings) and are used to provide structured data for the generated static site and for interoperability with other model management tools.

## Overview

- **File naming**: `<model_name>.metadata.json` (e.g., `my_lora.safetensors` → `my_lora.metadata.json`)
- **Format**: JSON with UTF-8 encoding
- **Purpose**: Store model metadata, tags, descriptions, triggers, and technical data.
- **Interoperability**: This format follows the standard used by popular model management tools, ensuring your LoraCamp catalog remains compatible with broader ecosystems.

---

## Base Fields (All Model Types)

These fields are generally present in all model metadata files.

| Field              | Type          | Required | LoraCamp Behavior | Description                                                                                    |
| :----------------- | :------------ | :------- | :---------------- | :--------------------------------------------------------------------------------------------- |
| `file_name`        | string        | ✅ Yes    | Generated         | Filename without extension (e.g., `"my_lora"`).                                                |
| `model_name`       | string        | ✅ Yes    | Displayed         | Display name of the model. Defaults to manifest `title` or `file_name`.                        |
| `file_path`        | string        | ✅ Yes    | Internal          | Path to the model file on the local filesystem.                                                |
| `size`             | integer       | ✅ Yes    | Displayed         | File size in bytes.                                                                            |
| `modified`         | float         | ✅ Yes    | Internal          | Unix timestamp when the model was imported or last modified.                                   |
| `sha256`           | string        | ✅ Yes    | Verified          | SHA256 hash of the model file (lowercase).                                                    |
| `base_model`       | string        | ❌ No     | Displayed         | Base model type (e.g., `"SD 1.5"`, `"SDXL"`, `"Flux.1"`).                                      |
| `preview_url`      | string        | ❌ No     | Processed         | URL or local path to the preview. Local paths are resolved to site-hosted URLs at build time.  |
| `notes`            | string        | ❌ No     | Displayed         | Detailed notes or "About" text. Mapped from manifest `about`.                                  |
| `tags`             | array[string] | ❌ No     | Processed         | Model tags for categorization.                                                                 |
| `modelDescription` | string        | ❌ No     | Displayed         | Full model description. Often mirrors `notes` in LoraCamp.                                     |
| `metadata_source`  | string        | ❌ No     | Internal          | Tracks the source of metadata (e.g., `"loracamp"`, `"civitai_api"`). Not shown on static site. |

---

## Model-Specific Fields

### LoRA Models

| Field | Type | Description |
|-------|------|-------------|
| `usage_tips` | string (JSON) | JSON string containing recommended usage parameters (strengths, CLIP skip). |

**`usage_tips` JSON structure:**

```json
{
  "strength_min": 0.3,
  "strength_max": 0.8,
  "strength_range": "0.3-0.8",
  "strength": 0.6,
  "clip_strength": 0.5,
  "clip_skip": 2
}
```

---

### Checkpoint & Embedding Models

| Field | Type | Description |
|-------|------|-------------|
| `model_type` | string | `"checkpoint"` or `"embedding"`. |

---

## The `civitai` Field Structure

LoraCamp preserves the `civitai` object for compatibility and extracts several key fields for the static site. Fields listed under this object often come directly from the Civitai API response.

### Key Fields Used by LoraCamp

| Field          | Type           | Description                                                        |
| :------------- | :------------- | :----------------------------------------------------------------- |
| `trainedWords` | array[string]  | **Trigger Words** used to activate the LoRA in prompts.             |
| `creator`      | object         | Information about the author (e.g., `creator.username`).           |
| `images`       | array[object]  | Example images showing the model's output, often includes prompts. |
| `model`        | object         | Parent model details, including broader `tags` and `description`.   |

> [!NOTE]
> Any other fields present in the `civitai` object (such as `id`, `downloadUrl`, or `nsfwLevel`) are preserved in the original `.metadata.json` file but are not currently displayed or used by LoraCamp.

## Metadata Merging & Precedence

LoraCamp treats an existing `<model>.metadata.json` as the "final word" for fields it contains. However, if specific information is missing from the JSON but available in `model.toml`, `creator.toml`, or the file itself (like SHA256), LoraCamp will **fill in the gaps** at build time.

1. **`metadata.json`**: Primary source (if non-empty).
2. **`model.toml`**: Fallback/Gap-fill.
3. **`creator.toml`**: Fallback for author information.
4. **File Data**: Fallback for technical fields (size, hash).

> [!IMPORTANT]
> LoraCamp will NOT overwrite your existing `metadata.json` file if it exists. It only generates a new one if it is missing.

---

## Version History

| 1.1     | 2026-03 | Clarified field support and added `trainedWords` detail |
| 1.0     | 2026-03 | LoraCamp integration of the metadata schema             |
