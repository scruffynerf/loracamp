import pytest
from loracamp.validators import validate_manifest

def test_validate_catalog_valid():
    data = {
        "title": "A Title",
        "creator": "Someone",
        "base_url": "https://example.com"
    }
    errors = validate_manifest("catalog.toml", data)
    assert not errors # should be empty

def test_validate_catalog_invalid():
    data = {
        "title": 123, # invalid type
        "creator": "Someone",
        "base_url": "https://example.com"
    }
    errors = validate_manifest("catalog.toml", data)
    assert "title" in errors
    assert errors["title"] == "expected string"

def test_validate_model_valid():
    data = {
        "title": "Model",
        "unlisted": True,
        "previews": ["1.jpg"]
    }
    errors = validate_manifest("model.toml", data)
    assert not errors

def test_validate_unknown_manifest():
    data = {"title": "Unknown"}
    errors = validate_manifest("unknown.toml", data)
    assert not errors # Returns empty dict for unknown manifests according to implementation
