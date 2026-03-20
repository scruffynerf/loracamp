import pytest
import os
from pathlib import Path
from loracamp.engine import LoraCampEngine
from loracamp.theming import generate_theme_css, _dark_palette, _light_palette

def test_generate_theme_css_default():
    css = generate_theme_css(None)
    assert "<style>" in css
    assert ":root" in css
    assert "--bg-1" in css
    assert "--cover-border-radius: 0;" in css

def test_generate_theme_css_light_mode():
    theme = {"base": "light", "accent_hue": 0, "accent_chroma": 50, "round_corners": True}
    css = generate_theme_css(theme)
    assert "--cover-border-radius: 0.4rem;" in css
    # Light palette generates specific lightness values
    assert "hsl(0, 5%, 97%)" in css

def test_generate_theme_css_dark_mode():
    theme = {"base": "dark", "accent_hue": 210, "accent_chroma": 40}
    css = generate_theme_css(theme)
    assert "hsl(210, 4%, 10%)" in css  # --bg-1 for dark mode with hue 210, chroma 40 -> cs = 0.4 -> 4%

def test_dark_palette():
    palette = _dark_palette(200, 100) # cs = 1.0 -> 10% saturation for bg-1
    assert palette["--bg-1"] == "hsl(200, 10%, 10%)"

def test_light_palette():
    palette = _light_palette(100, 10)  # cs = 0.1 -> 1% saturation for bg-1
    assert palette["--bg-1"] == "hsl(100, 1%, 97%)"

def test_site_assets_custom_css(tmp_path):
    """Test that custom CSS listed in site_assets is copied and linked."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    
    # Create catalog.toml with site_assets
    (catalog_dir / "catalog.toml").write_text(
        'title = "Test Catalog"\n'
        'creator = "Tester"\n'
        'base_url = "http://test.com"\n'
        'site_assets = ["theme1.css", "theme2.css", "logo.png"]'
    )
    
    # Create the assets
    (catalog_dir / "theme1.css").write_text(":root { --theme1: 1; }")
    (catalog_dir / "theme2.css").write_text(":root { --theme2: 2; }")
    (catalog_dir / "logo.png").touch()
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    # Check that CSS files were copied to static/css/
    assert (output_dir / "yoursite" / "static" / "css" / "theme1.css").exists()
    assert (output_dir / "yoursite" / "static" / "css" / "theme2.css").exists()
    
    # Check that other assets were copied to static/assets/
    assert (output_dir / "yoursite" / "static" / "assets" / "logo.png").exists()
    
    # Check that index.html contains both links
    index_content = (output_dir / "yoursite" / "index.html").read_text()
    assert 'static/css/theme1.css' in index_content
    assert 'static/css/theme2.css' in index_content

def test_legacy_custom_css(tmp_path):
    """Test that custom.css is still handled even if not in site_assets (legacy)."""
    catalog_dir = tmp_path / "catalog"
    catalog_dir.mkdir()
    
    (catalog_dir / "catalog.toml").write_text('title = "Test"\ncreator = "T"\nbase_url = "http://t.com"')
    (catalog_dir / "custom.css").write_text(".custom { color: red; }")
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    engine = LoraCampEngine(catalog_dir, output_dir)
    engine.build()
    
    assert (output_dir / "yoursite" / "static" / "css" / "custom.css").exists()
    index_content = (output_dir / "yoursite" / "index.html").read_text()
    assert 'static/css/custom.css' in index_content
