import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
from .manifests import CatalogManifest, ModelManifest, parse_catalog, parse_model
from .metadata import generate_metadata_json, save_metadata
from .assets import copy_static_assets
from .cdn import resolve_file_url, should_go_to_cdn

class LoraCampEngine:
    def __init__(self, catalog_dir: Path, output_dir: Path, cdn_url: Optional[str] = None):
        self.catalog_dir = catalog_dir
        self.output_dir = output_dir
        self.cdn_url = cdn_url
        
        # By default, everything goes into the output_dir root
        # If CDN splitting is needed, we'll use subdirs
        self.site_dir = output_dir
        self.asset_dir = output_dir
        
        if cdn_url:
            self.site_dir = output_dir / "yoursite"
            self.asset_dir = output_dir / "yourassets"
        
        # Initialize Jinja2
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def build(self):
        print(f"Building LoraCamp site in {self.site_dir}...")
        
        # 1. Setup directories
        self.site_dir.mkdir(parents=True, exist_ok=True)
        if self.cdn_url:
            self.asset_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Copy static assets
        copy_static_assets(self.site_dir)
        
        # 3. Parse Global Catalog
        catalog_manifest_path = self.catalog_dir / "catalog.toml"
        catalog = None
        if catalog_manifest_path.exists():
            catalog = parse_catalog(catalog_manifest_path)
            
        # 4. Walk directory for Models
        models = []
        for root, dirs, files in os.walk(self.catalog_dir):
            root_path = Path(root)
            
            # Look for .safetensors to identify a Model
            safetensors = [f for f in files if f.endswith(".safetensors")]
            if safetensors:
                model_data = self.process_model(root_path, safetensors, catalog)
                models.append(model_data)
        
        # 5. Render Index
        self.render_index(catalog, models)
        
        print("Build complete!")

    def process_model(self, model_dir: Path, safetensor_files: List[str], catalog: Optional[CatalogManifest]):
        manifest_path = model_dir / "model.toml"
        if manifest_path.exists():
            model_manifest = parse_model(manifest_path)
        else:
            model_manifest = ModelManifest(title=model_dir.name)
            
        model_slug = model_manifest.permalink or model_dir.name
        model_site_dir = self.site_dir / model_slug
        model_site_dir.mkdir(parents=True, exist_ok=True)

        # 1. Generate Metadata JSON
        main_model_file = model_dir / safetensor_files[0]
        meta_json = generate_metadata_json(model_manifest, main_model_file)
        save_metadata(meta_json, model_site_dir / "metadata.json")

        # 2. Handle Preview Image
        preview_url = None
        preview_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        for f in model_dir.iterdir():
            if f.stem.lower() in ("cover", "preview") and f.suffix.lower() in preview_extensions:
                from .media import optimize_image
                preview_dest = model_site_dir / "preview.jpg"
                if optimize_image(f, preview_dest):
                    preview_url = "preview.jpg"
                break
        
        # 3. Handle Asset Placement (Local vs CDN)
        model_filename = main_model_file.name
        
        if self.cdn_url:
            # Split mode
            model_asset_path = Path(model_slug) / model_filename
            dest_asset = self.asset_dir / model_asset_path
            dest_asset.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(main_model_file, dest_asset)
            model_url = f"{self.cdn_url.rstrip('/')}/{model_asset_path}"
        else:
            # Combined mode
            dest_path = model_site_dir / model_filename
            import shutil
            shutil.copy2(main_model_file, dest_path)
            model_url = model_filename

        # 3. Discover Samples (MP3, WAV, FLAC)
        samples = []
        audio_extensions = {".mp3", ".wav", ".flac"}
        for f in model_dir.iterdir():
            if f.suffix.lower() in audio_extensions:
                sample_data = self.process_sample(f, model_slug, model_manifest)
                samples.append(sample_data)

        # 4. Render Detail Page
        self.render_model_page(model_manifest, samples, model_url, preview_url, model_site_dir)

        # Build list of creators for the index
        display_creator = model_manifest.creator
        if not display_creator and model_manifest.creators:
            display_creator = ", ".join(model_manifest.creators)
        elif not display_creator and catalog:
            display_creator = catalog.creator

        return {
            "manifest": model_manifest,
            "model_url": model_url,
            "preview_url": preview_url,
            "display_creator": display_creator,
            "dir": model_dir,
            "slug": model_slug
        }

    def process_sample(self, audio_file: Path, model_slug: str, model_manifest: ModelManifest):
        from .media import transcode_audio, get_audio_duration
        
        # Output to SLUG/samples/filename.mp3
        if self.cdn_url:
            sample_asset_path = Path(model_slug) / "samples" / (audio_file.stem + ".mp3")
            dest_asset = self.asset_dir / sample_asset_path
            dest_asset.parent.mkdir(parents=True, exist_ok=True)
            transcode_dest = dest_asset
        else:
            sample_rel_path = Path("samples") / (audio_file.stem + ".mp3")
            dest_path = (self.site_dir / model_slug / sample_rel_path)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            transcode_dest = dest_path

        print(f"  Transcoding sample: {audio_file.name} -> {transcode_dest.name}")
        transcode_audio(audio_file, transcode_dest, title=audio_file.stem, creator=model_manifest.creator)
        
        duration = get_audio_duration(transcode_dest)
        
        if self.cdn_url:
            sample_url = f"{self.cdn_url.rstrip('/')}/{sample_asset_path}"
        else:
            sample_url = f"samples/{transcode_dest.name}"
            
        return {
            "name": audio_file.stem,
            "url": sample_url,
            "duration": duration
        }

    def render_model_page(self, model_manifest: ModelManifest, samples: List[Dict], model_url: str, preview_url: Optional[str], output_dir: Path):
        try:
            template = self.env.get_template("model.html")
        except:
            # Fallback index if model.html not ready
            return
            
        content = template.render(model=model_manifest, samples=samples, model_url=model_url, preview_url=preview_url)
        with open(output_dir / "index.html", "w") as f:
            f.write(content)

    def render_index(self, catalog: Optional[CatalogManifest], models: List[Dict]):
        template = self.env.get_template("index.html")
        content = template.render(catalog=catalog, models=models)
        with open(self.site_dir / "index.html", "w") as f:
            f.write(content)
