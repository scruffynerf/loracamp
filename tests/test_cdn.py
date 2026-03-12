import pytest
from pathlib import Path
from loracamp.cdn import resolve_file_url, should_go_to_cdn

def test_resolve_file_url_local():
    file_path = Path("/mock/catalog/my_model/model.safetensors")
    catalog_dir = Path("/mock/catalog")
    
    url = resolve_file_url(file_path, catalog_dir)
    assert url == "../my_model/model.safetensors"

def test_resolve_file_url_cdn():
    file_path = Path("/mock/catalog/my_model/model.safetensors")
    catalog_dir = Path("/mock/catalog")
    cdn_url = "https://cdn.example.com/"
    
    url = resolve_file_url(file_path, catalog_dir, cdn_url)
    assert url == "https://cdn.example.com/my_model/model.safetensors"

def test_should_go_to_cdn():
    assert should_go_to_cdn(Path("model.safetensors")) is True
    assert should_go_to_cdn(Path("sample.mp3")) is True
    assert should_go_to_cdn(Path("archive.zip")) is True
    assert should_go_to_cdn(Path("index.html")) is False
    assert should_go_to_cdn(Path("style.css")) is False
    assert should_go_to_cdn(Path("preview.jpg")) is False
