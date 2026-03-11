import tomli
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path

@dataclass
class BaseModel:
    title: Optional[str] = None
    synopsis: Optional[str] = None
    more: Optional[str] = None
    links: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class CatalogManifest(BaseModel):
    base_url: Optional[str] = None
    cdn_url: Optional[str] = None
    language: str = "en"
    faircamp_signature: bool = True
    favicon: Optional[str] = None
    site_assets: List[str] = field(default_factory=list)
    site_metadata: Optional[str] = None

@dataclass
class ModelManifest(BaseModel):
    about: Optional[str] = None
    trigger_word: Optional[str] = None
    creator: Optional[str] = None
    creators: List[str] = field(default_factory=list) # Supporting multiple creators
    release_date: Optional[str] = None
    release_creators: List[str] = field(default_factory=list) # Faircamp compatibility
    permalink: Optional[str] = None
    preview: Optional[str] = None
    previews: List[str] = field(default_factory=list) # Additional preview images
    unlisted: bool = False
    base_model: Optional[str] = None # e.g., "SD 1.5", "SDXL"
    version: Optional[str] = None # e.g., "v1.0"
    sample_prompts: List[str] = field(default_factory=list)

@dataclass
class SampleManifest(BaseModel):
    creator: Optional[str] = None
    creators: List[str] = field(default_factory=list)
    sample_number: Optional[int] = None
    # In LoraCamp, samples are usually associated with a specific file
    file: Optional[str] = None
    about: Optional[str] = None
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None
    model: Optional[str] = None
    vae: Optional[str] = None
    clip: Optional[str] = None
    loras: List[Dict[str, Any]] = field(default_factory=list)
    steps: Optional[int] = None
    cfg: Optional[float] = None
    sampler: Optional[str] = None
    scheduler: Optional[str] = None
    workflow: Optional[str] = None
    shift: Optional[float] = None
    lyrics: Optional[str] = None
    keyscale: Optional[str] = None
    bpm: Optional[float] = None
    timesignature: Optional[str] = None
    language: Optional[str] = None
    additional_seed: Optional[int] = None
    llm_cfg: Optional[float] = None
    llm_temp: Optional[float] = None
    llm_top_p: Optional[float] = None
    llm_top_k: Optional[int] = None
    llm_min_p: Optional[float] = None
    llm_rep_penalty: Optional[float] = None

def load_toml(path: Path) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return tomli.load(f)

def parse_catalog(path: Path) -> CatalogManifest:
    data = load_toml(path)
    return CatalogManifest(**data)

def parse_model(path: Path) -> ModelManifest:
    data = load_toml(path)
    return ModelManifest(**data)

def parse_sample(path: Path) -> SampleManifest:
    data = load_toml(path)
    return SampleManifest(**data)
