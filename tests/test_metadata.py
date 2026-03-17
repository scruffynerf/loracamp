import pytest
import json
from pathlib import Path
from loracamp.metadata import generate_metadata_json, calculate_sha256, extract_safetensors_metadata
from loracamp.manifests import ModelManifest

def test_calculate_sha256(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"hello world")
    
    hash_val = calculate_sha256(file_path)
    assert hash_val == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

def test_generate_metadata_json():
    manifest = ModelManifest(
        title="My Model",
        about="A good model",
        trigger_word="oh yeah"
    )
    
    json_str = generate_metadata_json(manifest, None)
    data = json.loads(json_str)
    
    assert data["model_name"] == "My Model"
    assert data["notes"] == "A good model"
    assert data["civitai"]["trainedWords"] == ["oh yeah"]
    assert "sha256" in data

def test_generate_metadata_json_with_file(tmp_path: Path):
    manifest = ModelManifest(
        title="My File Model",
    )
    
    file_path = tmp_path / "test.safetensors"
    # Create a dummy file
    file_path.write_bytes(b"dummy data")
    
    json_str = generate_metadata_json(manifest, file_path)
    data = json.loads(json_str)
    
    assert data["model_name"] == "My File Model"
    assert data["file_name"] == "test"
    assert "sha256" in data
    assert data["size"] == len(b"dummy data")
