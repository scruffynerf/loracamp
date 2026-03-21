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
    """
    try:
        with open(file_path, "rb") as f:
            length_bytes = f.read(8)
            if len(length_bytes) < 8:
                return None
            (header_len,) = struct.unpack("<Q", length_bytes)
            if header_len <= 0 or header_len > 100 * 1024 * 1024:
                return None
                
            header_bytes = f.read(header_len)
            header_str = header_bytes.decode("utf-8")
            header_data = json.loads(header_str)
            return header_data.get("__metadata__", {})
    except Exception as e:
        print(f"Error extracting safetensors metadata from {file_path.name}: {e}")
        return None

def load_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON metadata from file."""
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"  [ERROR] Loading metadata from {file_path.name}: {e}")
    return None

def validate_metadata(data: Dict[str, Any]) -> list[str]:
    """Validate metadata against the JSON schema."""
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema library not installed."]
        
    schema_path = Path(__file__).parent / "specs" / "metadata.schema.json"
    if not schema_path.exists():
        return ["Metadata schema file not found in loracamp/specs/"]
    
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.validate(instance=data, schema=schema)
        return []
    except Exception as e:
        # Return a simple list of errors
        return [str(e)]

def merge_metadata(existing_data: Dict[str, Any], manifest_data: Dict[str, Any], tech_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fill in gaps in existing_data using manifest_data and tech_data.
    Do NOT overwrite existing non-empty values.
    """
    merged = existing_data.copy()
    
    # 1. Handle top-level gaps
    for key, value in tech_data.items():
        if key not in merged or merged[key] in (None, "", [], {}):
            merged[key] = value

    for key, value in manifest_data.items():
        if key not in merged or merged[key] in (None, "", [], {}):
            merged[key] = value

    # 2. Handle nested civitai gaps if they exist in source
    if "civitai" in manifest_data and isinstance(manifest_data["civitai"], dict):
        if "civitai" not in merged:
            merged["civitai"] = {}
        for c_key, c_value in manifest_data["civitai"].items():
            if c_key not in merged["civitai"] or not merged["civitai"][c_key]:
                merged["civitai"][c_key] = c_value
                
    return merged

def generate_metadata_json(
    model_manifest: ModelManifest, 
    safetensor_path: Optional[Path] = None
) -> str:
    """
    Assemble initial metadata JSON combining manifest data and technical data.
    """
    import time
    
    tech_data = {
        "file_name": safetensor_path.stem if safetensor_path else model_manifest.title,
        "file_path": str(safetensor_path.absolute()) if safetensor_path else "",
        "size": safetensor_path.stat().st_size if safetensor_path and safetensor_path.exists() else 0,
        "modified": safetensor_path.stat().st_mtime if safetensor_path and safetensor_path.exists() else time.time(),
        "sha256": calculate_sha256(safetensor_path) if safetensor_path and safetensor_path.exists() else "",
        "hash_status": "completed" if safetensor_path else "pending"
    }

    metadata = {
        "file_name": tech_data["file_name"],
        "model_name": model_manifest.title or tech_data["file_name"],
        "file_path": tech_data["file_path"],
        "size": tech_data["size"],
        "modified": tech_data["modified"],
        "sha256": tech_data["sha256"],
        "base_model": model_manifest.base_model or "Unknown",
        "preview_url": "", 
        "notes": model_manifest.about or "",
        "civitai": {
            "trainedWords": [model_manifest.trigger_word] if model_manifest.trigger_word else []
        },
        "tags": model_manifest.tags or [],
        "modelDescription": model_manifest.about or "",
        "metadata_source": "loracamp",
        "usage_tips": "{}"
    }
            
    return json.dumps(metadata, indent=2)

def save_metadata(json_content: str, output_path: Path):
    """Save the metadata JSON to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_content)
