import hashlib
import json
import struct
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

def extract_safetensors_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Read the JSON header from a .safetensors file.
    The first 8 bytes are an unsigned little-endian 64-bit integer representing the JSON header length N.
    The next N bytes are the JSON header string.
    """
    try:
        with open(file_path, "rb") as f:
            length_bytes = f.read(8)
            if len(length_bytes) < 8:
                return None
            (header_len,) = struct.unpack("<Q", length_bytes)
            if header_len <= 0 or header_len > 100 * 1024 * 1024: # Sanity check (max 100MB header)
                return None
                
            header_bytes = f.read(header_len)
            header_str = header_bytes.decode("utf-8")
            header_data = json.loads(header_str)
            
            # The general metadata in safetensors is usually under the "__metadata__" key
            return header_data.get("__metadata__", {})
    except Exception as e:
        print(f"Error extracting safetensors metadata from {file_path.name}: {e}")
        return None

def generate_metadata_json(
    model_manifest: ModelManifest, 
    safetensor_path: Optional[Path] = None
) -> str:
    """
    Assemble metadata JSON combining manifest data and technical data (SHA256, Safetensor __metadata__).
    """
    metadata = {
        "file_name": safetensor_path.stem if safetensor_path else model_manifest.title,
        "model_name": model_manifest.title,
        "size": safetensor_path.stat().st_size if safetensor_path and safetensor_path.exists() else 0,
        "modified": safetensor_path.stat().st_mtime if safetensor_path and safetensor_path.exists() else 0,
        "sha256": calculate_sha256(safetensor_path) if safetensor_path and safetensor_path.exists() else "",
        "base_model": model_manifest.base_model or "Other",
        "preview_url": "", # Optional logic could be added here later if needed
        "preview_nsfw_level": 0,
        "notes": model_manifest.about or "",
        "from_civitai": False,
        "civitai": {
            "trainedWords": [model_manifest.trigger_word] if model_manifest.trigger_word else []
        },
        "tags": model_manifest.tags or [],
        "modelDescription": model_manifest.about or "",
        "civitai_deleted": False,
        "favorite": False,
        "exclude": False,
        "db_checked": False,
        "skip_metadata_refresh": False,
        "metadata_source": "loracamp",
        "last_checked_at": 0,
        "usage_tips": "{}"
    }
            
    return json.dumps(metadata, indent=2)

def save_metadata(json_content: str, output_path: Path):
    """Save the metadata JSON to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_content)
