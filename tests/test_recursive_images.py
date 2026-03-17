import pytest
from pathlib import Path
from loracamp.engine import LoraCampEngine
import os
import shutil

def test_recursive_image_discovery(tmp_path):
    """Verify that images in subdirectories are discovered for Image Loras."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "Tester"\nbase_url = "http://test.com"')
    
    lora_dir = catalog_dir / "recursive-lora"
    lora_dir.mkdir()
    (lora_dir / "model.toml").write_text('title = "Recursive Lora"')
    (lora_dir / "model.safetensors").touch()
    (lora_dir / "preview.png").touch()
    
    # Nested samples
    nested_dir = lora_dir / "more_samples" / "sub"
    nested_dir.mkdir(parents=True)
    (nested_dir / "nested_img.jpg").touch()
    (lora_dir / "samples" / "flat_img.webp").mkdir(parents=True, exist_ok=True)
    (lora_dir / "samples" / "flat_img.webp").rmdir() # Oops, I want a file
    (lora_dir / "samples" / "flat_img.webp").touch()
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    site_lora_dir = output_dir / "yoursite" / "recursive-lora"
    
    # Check that indices exist
    assert (site_lora_dir / "index.html").exists()
    
    # Verify both images are copied and have safe names
    # Flat image
    assert (site_lora_dir / "flat_img.webp").exists()
    # Nested image - should be flattened with underscore
    # Path was recursive-lora/more_samples/sub/nested_img.jpg
    # parts rel to model_dir: ('more_samples', 'sub', 'nested_img.jpg')
    # safe_name: more_samples_sub_nested_img.jpg
    assert (site_lora_dir / "more_samples_sub_nested_img.jpg").exists()
    
    page_content = (site_lora_dir / "index.html").read_text()
    assert 'flat_img.webp' in page_content
    assert 'more_samples_sub_nested_img.jpg' in page_content

def test_image_metadata_extraction_mock(tmp_path):
    """Test the metadata extraction logic with a mock-like approach if possible."""
    # Since we can't easily forge a real PNG with tEXt chunks without PIL here,
    # we'll test the logic by calling the function on a plain file and expecting {}
    # and then perhaps mocking it.
    from loracamp.media import extract_image_metadata
    
    plain_file = tmp_path / "test.png"
    plain_file.touch()
    
    # Should not crash on invalid image or empty image
    meta = extract_image_metadata(plain_file)
    assert isinstance(meta, dict)
