import pytest
import os
import shutil
from pathlib import Path
from loracamp.engine import LoraCampEngine

def test_engine_build_real_catalog(tmp_path):
    """Test building the actual test_catalog to verify manifest processing."""
    # Source is our workspace test_catalog
    catalog_dir = Path(__file__).parent.parent / "test_catalog"
    if not catalog_dir.exists():
        pytest.skip("test_catalog not found in workspace")
    
    output_dir = tmp_path / "build"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    # 1. Verify index.html exists
    assert (output_dir / "yoursite" / "index.html").exists()
    
    # 2. Verify model pages exist
    assert (output_dir / "yoursite" / "cool-lora" / "index.html").exists()
    assert (output_dir / "yoursite" / "image-only-lora" / "index.html").exists()
    
    # 3. Verify search_data.json exists
    assert (output_dir / "yoursite" / "search_data.json").exists()
    
    # 4. Check contents of index.html for title
    index_content = (output_dir / "yoursite" / "index.html").read_text()
    assert "LoraCamp Test Catalog" in index_content

def test_engine_image_lora_detection(tmp_path):
    """Specific test for Image Lora detection logic."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "Tester"\nbase_url = "http://test.com"')
    
    # Create an image-only lora
    lora_dir = catalog_dir / "img-lora"
    lora_dir.mkdir()
    (lora_dir / "model.toml").write_text('title = "Img Lora"')
    (lora_dir / "model.safetensors").touch()
    (lora_dir / "preview.png").touch()
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    # Look for clue in the generated page - the gallery dive
    model_page = (output_dir / "yoursite" / "img-lora" / "index.html").read_text()
    assert 'class="image-gallery"' in model_page
    assert 'class="tracks"' not in model_page

def test_engine_creator_detection(tmp_path):
    """Test that creator pages are generated correctly."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "Tester"\nbase_url = "http://test.com"')
    
    # Create creator folder
    creator_dir = catalog_dir / "MyCreator"
    creator_dir.mkdir()
    (creator_dir / "creator.toml").write_text('name = "MyCreator"\npermalink = "mc"')
    
    # Create a lora by this creator
    lora_dir = catalog_dir / "lora1"
    lora_dir.mkdir()
    (lora_dir / "model.toml").write_text('title = "Lora1"\ncreator = "MyCreator"')
    (lora_dir / "model.safetensors").touch()
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    # Verify creator page
    assert (output_dir / "yoursite" / "mc" / "index.html").exists()
    creator_page = (output_dir / "yoursite" / "mc" / "index.html").read_text()
    assert "Lora1" in creator_page
