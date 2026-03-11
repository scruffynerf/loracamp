from static_ffmpeg import add_paths
import ffmpegio
from pathlib import Path
from typing import Optional

# Add ffmpeg/ffprobe to the PATH automatically
add_paths()

def transcode_audio(
    input_path: Path, 
    output_path: Path, 
    title: Optional[str] = None,
    creator: Optional[str] = None
) -> bool:
    """
    Transcode an audio file to MP3 VBR 0 (highest quality) using ffmpegio.
    Adds basic metadata tags.
    """
    options = {
        "codec:a": "libmp3lame",
        "qscale:a": "0", # VBR 0
        "map_metadata": "-1" # Start clean
    }
    
    metadata = {}
    if title:
        metadata["title"] = title
    if creator:
        metadata["artist"] = creator
        
    try:
        ffmpegio.transcode(str(input_path), str(output_path), overwrite=True, **options, metadata=metadata)
        return True
    except Exception as e:
        print(f"Transcoding error: {e}")
        return False

def get_audio_duration(file_path: Path) -> Optional[float]:
    """Get the duration of an audio file using ffmpegio probe."""
    try:
        info = ffmpegio.probe.full_details(str(file_path))
        return float(info["format"]["duration"])
    except Exception as e:
        print(f"Probe error: {e}")
        return None

def optimize_image(input_path: Path, output_path: Path, max_size: int = 800):
    """Resize and optimize an image using Pillow."""
    from PIL import Image
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (e.g. for RGBA -> JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.thumbnail((max_size, max_size))
            img.save(output_path, "JPEG", quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"Image optimization error: {e}")
        return False
