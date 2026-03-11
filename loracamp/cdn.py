from pathlib import Path
from typing import Optional

def resolve_file_url(
    file_path: Path, 
    catalog_dir: Path, 
    cdn_url: Optional[str] = None
) -> str:
    """
    Resolve the URL for a file. 
    If cdn_url is provided, it returns a remote URL.
    Otherwise, it returns a relative path for local static hosting.
    """
    relative_path = file_path.relative_to(catalog_dir)
    
    if cdn_url:
        # Standardize cdn_url trailing slash
        base = cdn_url.rstrip("/")
        return f"{base}/{relative_path}"
    
    # For local static, we use relative paths in the HTML
    return f"../{relative_path}" # Assuming one level deep for Loras

def should_go_to_cdn(file_path: Path) -> bool:
    """
    Heuristic: large files (.safetensors, .mp3) go to CDN.
    Small assets (HTML, CSS, thumbnails) stay on the static site.
    """
    cdn_extensions = {".safetensors", ".mp3", ".zip", ".wav"}
    return file_path.suffix.lower() in cdn_extensions
