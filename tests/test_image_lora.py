import pytest
from pathlib import Path
from loracamp.engine import LoraCampEngine

def test_image_lora_download_links(tmp_path):
    """Verify that Image Loras include the original preview in downloads."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "Tester"\nbase_url = "http://test.com"')
    
    lora_dir = catalog_dir / "img-lora"
    lora_dir.mkdir()
    (lora_dir / "model.toml").write_text('title = "Img Lora"')
    (lora_dir / "model.safetensors").touch()
    (lora_dir / "preview.png").touch()
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    # Check the page content for download links
    page_content = (output_dir / "yoursite" / "img-lora" / "index.html").read_text()
    
    # It should have the model download
    assert 'Download Model' in page_content
    # It should have the original preview download as requested
    assert 'Download Preview Art (preview.png)' in page_content
    # It should have metadata
    assert 'Download Metadata' in page_content

def test_image_lora_gallery_inclusion(tmp_path):
    """Verify that the main preview is included in the gallery for image-only loras."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "Tester"\nbase_url = "http://test.com"')
    
    lora_dir = catalog_dir / "img-lora"
    lora_dir.mkdir()
    (lora_dir / "model.toml").write_text('title = "Img Lora"')
    (lora_dir / "model.safetensors").touch()
    (lora_dir / "preview.png").touch() # Main preview
    samples_dir = lora_dir / "samples"
    samples_dir.mkdir()
    (samples_dir / "extra.png").touch() # Additional sample
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    page_content = (output_dir / "yoursite" / "img-lora" / "index.html").read_text()
    
    # Verify BOTH images are in the gallery
    assert 'data-src="preview.png"' in page_content
    assert 'data-src="extra.png"' in page_content
