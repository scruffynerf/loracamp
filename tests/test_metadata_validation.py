import pytest
import json
from pathlib import Path
from loracamp.metadata import validate_metadata, merge_metadata, generate_metadata_json, load_metadata
from loracamp.manifests import ModelManifest

def test_metadata_validation_valid():
    data = {
        "file_name": "test_model",
        "model_name": "Test Model",
        "file_path": "/path/to/test_model.safetensors",
        "size": 1024,
        "modified": 123456789.0,
        "sha256": "0" * 64,
        "base_model": "SD 1.5",
        "metadata_source": "loracamp"
    }
    errors = validate_metadata(data)
    if errors:
        print(f"Validation Errors: {errors}")
    assert len(errors) == 0, f"Valid metadata validation failed: {errors}"

def test_metadata_validation_invalid():
    data = {
        "file_name": 123, # Should be string
        "model_name": "Test Model"
    }
    errors = validate_metadata(data)
    assert len(errors) > 0
    assert any("file_name" in err for err in errors)

def test_merge_metadata_gaps():
    existing = {
        "model_name": "Existing",
        "notes": ""
    }
    manifest_data = {
        "model_name": "Manifest Title",
        "notes": "Manifest About"
    }
    tech_data = {
        "sha256": "0" * 64,
        "size": 500
    }
    
    merged = merge_metadata(existing, manifest_data, tech_data)
    
    assert merged["model_name"] == "Existing" # No overwrite
    assert merged["notes"] == "Manifest About" # Gap filled
    assert merged["sha256"] == "0" * 64 # Tech gap filled

def test_generate_metadata_json():
    manifest = ModelManifest(title="Test LoRA", trigger_word="testword", base_model="SD 1.5")
    json_str = generate_metadata_json(manifest)
    data = json.loads(json_str)
    
    assert data["model_name"] == "Test LoRA"
    assert data["base_model"] == "SD 1.5"
    assert data["civitai"]["trainedWords"] == ["testword"]
    assert "preview_nsfw_level" not in data
    assert "favorite" not in data
    
    # Validate generated JSON
    errors = validate_metadata(data)
    if errors:
        print(f"Validation Errors: {errors}")
    assert len(errors) == 0, f"Generated metadata validation failed: {errors}"
