import pytest
from pathlib import Path
from xml.etree import ElementTree as ET
from loracamp.feeds import generate_atom_feed, generate_rss_feed
from loracamp.manifests import CatalogManifest, ModelManifest

@pytest.fixture
def mock_data():
    catalog = CatalogManifest(title="Test Catalog", synopsis="A test catalog that tests things.", language="en")
    
    manifest = ModelManifest(
        title="Test Model",
        about="This is a test model.",
        release_date="2025-01-01",
        creator="Test Author",
        base_model="SD 1.5"
    )
    
    models = [
        {
            "manifest": manifest,
            "slug": "test_model",
            "preview_url": "preview.jpg"
        }
    ]
    
    return catalog, models

def test_generate_atom_feed(tmp_path: Path, mock_data):
    catalog, models = mock_data
    output_path = tmp_path / "feed.atom"
    base_url = "https://example.com"
    
    generate_atom_feed(catalog, models, base_url, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    
    # Check for core Atom elements
    assert "xmlns=\"http://www.w3.org/2005/Atom\"" in content
    assert "<title>Test Catalog</title>" in content
    assert "href=\"https://example.com/feed.atom\"" in content
    assert "<entry>" in content
    assert "<title>Test Model</title>" in content
    assert "<name>Test Author</name>" in content
    assert "https://example.com/test_model/preview.jpg" in content
    assert "https://example.com/test_model/metadata.json" in content

def test_generate_rss_feed(tmp_path: Path, mock_data):
    catalog, models = mock_data
    output_path = tmp_path / "feed.rss"
    base_url = "https://example.com"
    
    generate_rss_feed(catalog, models, base_url, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    
    # Check for core RSS elements
    assert "<rss" in content
    assert "version=\"2.0\"" in content
    assert "<title>Test Catalog</title>" in content
    assert "<item>" in content
    assert "<title>Test Model</title>" in content
    assert "https://example.com/test_model/preview.jpg" in content
    
    # Check that the raw html descriptor worked for description with cdata
    assert "<![CDATA[" in content
    assert "📄 Metadata JSON" in content
