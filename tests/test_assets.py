import pytest
from pathlib import Path
from loracamp.assets import handle_custom_assets

def test_handle_custom_assets(tmp_path: Path):
    custom_dir = tmp_path / "custom"
    custom_dir.mkdir()
    (custom_dir / "my_script.js").write_text("console.log('hello');")
    
    custom_file = tmp_path / "image.png"
    custom_file.write_bytes(b"image data")
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    paths = [str(custom_dir), str(custom_file)]
    handle_custom_assets(paths, output_dir)
    
    # Assert custom folder contents were copied
    assert (output_dir / "custom" / "my_script.js").exists()
    assert (output_dir / "custom" / "my_script.js").read_text() == "console.log('hello');"
    
    # Assert single file was copied
    assert (output_dir / "image.png").exists()
    assert (output_dir / "image.png").read_bytes() == b"image data"
