import pytest
from pathlib import Path
from loracamp.manifests import (
    parse_catalog, 
    parse_model, 
    parse_creator, 
    parse_sample,
    CatalogManifest,
    ModelManifest,
    CreatorManifest,
    SampleManifest
)

def test_parse_catalog(tmp_path: Path):
    toml_file = tmp_path / "catalog.toml"
    toml_file.write_text('title = "My Catalog"\ncreator = "Scruffy"\nlanguage = "en"')
    
    catalog = parse_catalog(toml_file)
    assert isinstance(catalog, CatalogManifest)
    assert catalog.title == "My Catalog"
    assert catalog.creator == "Scruffy"
    assert catalog.language == "en"

def test_parse_model(tmp_path: Path):
    toml_file = tmp_path / "model.toml"
    toml_file.write_text('title = "My Model"\nunlisted = true\npreviews = ["a.jpg", "b.jpg"]')
    
    model = parse_model(toml_file)
    assert isinstance(model, ModelManifest)
    assert model.title == "My Model"
    assert model.unlisted is True
    assert model.previews == ["a.jpg", "b.jpg"]

def test_parse_creator(tmp_path: Path):
    toml_file = tmp_path / "creator.toml"
    toml_file.write_text('name = "Creator Name"\n[links]\nwebsite = "http://example.com"')
    
    creator = parse_creator(toml_file)
    assert isinstance(creator, CreatorManifest)
    assert creator.name == "Creator Name"
    assert creator.links_dict == {"website": "http://example.com"}

def test_parse_sample(tmp_path: Path):
    toml_file = tmp_path / "sample.toml"
    toml_file.write_text('title = "A sample"\nprompt = "A nice prompt"\nseed = 42')
    
    sample = parse_sample(toml_file)
    assert isinstance(sample, SampleManifest)
    assert sample.title == "A sample"
    assert sample.prompt == "A nice prompt"
    assert sample.seed == 42
