import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional
from .manifests import ModelManifest

def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in 4KB chunks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_metadata_json(
    model_manifest: ModelManifest, 
    safetensor_path: Optional[Path] = None
) -> str:
    """
    Assemble metadata JSON combining manifest data and technical data (SHA256).
    """
    metadata = {
        "title": model_manifest.title,
        "about": model_manifest.about,
        "trigger_word": model_manifest.trigger_word,
        "creator": model_manifest.creator,
        "release_date": model_manifest.release_date,
        "release_creators": model_manifest.release_creators,
    }
    
    if safetensor_path and safetensor_path.exists():
        metadata["technical"] = {
            "sha256": calculate_sha256(safetensor_path),
            "filename": safetensor_path.name,
            "size_bytes": safetensor_path.stat().st_size
        }
    
    return json.dumps(metadata, indent=4)

def save_metadata(json_content: str, output_path: Path):
    """Save the metadata JSON to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_content)
