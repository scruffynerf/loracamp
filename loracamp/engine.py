import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
from .manifests import CatalogManifest, ModelManifest, SampleManifest, CreatorManifest, parse_catalog, parse_model, parse_sample, parse_creator, load_toml
from .metadata import generate_metadata_json, save_metadata
from .assets import copy_static_assets
from .cdn import resolve_file_url, should_go_to_cdn
from .validators import validate_manifest
from .feeds import generate_atom_feed, generate_rss_feed
from .theming import generate_theme_css

class LoraCampEngine:
    def __init__(
        self,
        catalog_dir: Path,
        output_dir: Path,
        cdn_url: Optional[str] = None,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        debug_layout: bool = False,
    ):
        self.catalog_dir = catalog_dir
        self.output_dir = output_dir
        self.cdn_url = cdn_url
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.debug_layout = debug_layout
        self.creator_aliases: Dict[str, str] = {}
        self.theme_css: str = ""
        self.has_custom_css: bool = False
        self.custom_css_files: List[str] = []
        self.build_id = str(int(time.time()))
        
        # Set up explicit output folders for clarity
        self.site_dir = output_dir / "yoursite"
        self.asset_dir = output_dir / "yoursite"
        
        if cdn_url:
            self.asset_dir = output_dir / "yourcdn"
        
        # Initialize Jinja2
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Register custom filters
        import markdown
        self.env.filters["markdown"] = lambda t: markdown.markdown(t or "", extensions=['extra'])
    
    
    def _load_plugins(self):
        """Dynamically load Python files from the plugins/ directory."""
        plugins_dir = Path.cwd() / "plugins"
        if not plugins_dir.exists():
            return

        import importlib.util
        import sys
        
        print("Loading plugins...")
        for f in plugins_dir.glob("*.py"):
            if f.name == "__init__.py":
                continue
                
            try:
                module_name = f"loracamp_plugin_{f.stem}"
                spec = importlib.util.spec_from_file_location(module_name, f)
                if spec and spec.loader:
                    loader = spec.loader
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    loader.exec_module(module)  # type: ignore
                    
                    # Call register hook if exists
                    if hasattr(module, "register"):
                        module.register(self)
                    print(f"  Loaded: {f.name}")
            except Exception as e:
                print(f"  FAILED to load plugin {f.name}: {e}")

    def build(self):
        print(f"Building LoraCamp site in {self.site_dir}...")
        
        # 0. Load Plugins
        self._load_plugins()

        # 1. Setup directories
        self.site_dir.mkdir(parents=True, exist_ok=True)
        if self.cdn_url:
            self.asset_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Copy static assets
        copy_static_assets(self.site_dir)
        
        # 2a. Conditional debug cleanup
        if not self.debug_layout:
            debug_css_dest = self.site_dir / "static" / "css" / "debug.css"
            if debug_css_dest.exists():
                debug_css_dest.unlink()
        
        # 2b. Initial has_custom_css check will be finalized after catalog parsing
        self.env.globals["enable_opengraph"] = True # Default
        self.env.globals["enable_feeds"] = True   # Default
        
        # 3. Parse Global Catalog
        catalog_manifest_path = self.catalog_dir / "catalog.toml"
        catalog = None
        if catalog_manifest_path.exists():
            data = load_toml(catalog_manifest_path)
            errors = validate_manifest("catalog.toml", data)
            if errors:
                print(f"Validation errors in {catalog_manifest_path}:")
                for key, err in errors.items():
                    print(f"  - {key}: {err}")
                return # Abort build on catalog error
            catalog = parse_catalog(catalog_manifest_path)
            self.env.globals["enable_opengraph"] = catalog.opengraph if isinstance(catalog.opengraph, bool) else True
            self.env.globals["enable_feeds"] = catalog.feeds if isinstance(catalog.feeds, bool) else True

            # 3a. Handle site_assets (including custom CSS)
            if catalog.site_assets:
                import shutil
                for asset_name in catalog.site_assets:
                    asset_src = self.catalog_dir / asset_name
                    if asset_src.exists():
                        if asset_name.endswith(".css"):
                            dest = self.site_dir / "static" / "css" / asset_name
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(asset_src, dest)
                            self.custom_css_files.append(asset_name)
                            print(f"  Custom CSS asset: {asset_name}")
                        else:
                            # Other assets go to static/assets
                            dest = self.site_dir / "static" / "assets" / asset_name
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(asset_src, dest)
                            print(f"  Site asset: {asset_name}")
                    else:
                        print(f"  WARNING: Site asset '{asset_name}' not found in {self.catalog_dir}")

        # 3b. Legacy custom.css check (if not already added via site_assets)
        custom_css_path = self.catalog_dir / "custom.css"
        if custom_css_path.exists() and "custom.css" not in self.custom_css_files:
            import shutil
            dest = self.site_dir / "static" / "css" / "custom.css"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(custom_css_path, dest)
            self.custom_css_files.append("custom.css")
            print(f"  Detected legacy custom.css, copying to static assets...")

        self.has_custom_css = len(self.custom_css_files) > 0
        self.env.globals["has_custom_css"] = self.has_custom_css
        self.env.globals["custom_css_files"] = self.custom_css_files

        # 3b. Generate theme CSS from catalog config.
        # If the user has provided custom CSS via site_assets, skip generating
        # the inline theme block entirely. The custom CSS fully replaces it and
        # we want to avoid cascade conflicts.
        if self.custom_css_files:
            # Only inject the shared structural vars (border-radius, etc.) not colors
            theme_config = getattr(catalog, "theme", None) if catalog else None
            if theme_config:
                round_corners = theme_config.get("round_corners", False)
                border_radius = "0.4rem" if round_corners else "0"
                self.theme_css = f"<style>\n:root {{\n    --cover-border-radius: {border_radius};\n    --ul-list-style-type: disc;\n}}\n</style>"
            else:
                self.theme_css = ""
        else:
            theme_config = getattr(catalog, "theme", None) if catalog else None
            self.theme_css = generate_theme_css(theme_config)

        # 4. Walk directory for Models and Creators
        models = []
        creators = []
        for root, dirs, files in os.walk(self.catalog_dir):
            root_path = Path(root)

            # Compute the relative path from the catalog root for filtering.
            # The catalog root itself (rel == ".") is always visited regardless of filters
            # so that top-level catalog.toml is parsed and all subdirs are reachable.
            try:
                rel_path = root_path.relative_to(self.catalog_dir)
            except ValueError:
                rel_path = root_path
            rel_str = str(rel_path)
            is_catalog_root = rel_str == "."

            if not is_catalog_root:
                # Exclude: prune this subtree entirely and skip processing
                if any(p in rel_str for p in self.exclude_patterns):
                    dirs.clear()  # prevent os.walk from descending further
                    continue

                # Include: if patterns are given, skip dirs that match none of them.
                # Also prune subdirs so we don't waste time descending into excluded trees.
                if self.include_patterns and not any(p in rel_str for p in self.include_patterns):
                    dirs.clear()
                    continue

            print(f"Scanning: {root_path}")

            # Validate TOML filenames to catch user typos
            for f in files:
                if f.endswith(".toml"):
                    is_valid = f in ["catalog.toml", "model.toml", "creator.toml", "sample.toml"]
                    if not is_valid and not f.endswith(".sample.toml"):
                        print(f"  WARNING: Ignored invalid manifest name '{f}' in {root_path}. Valid names are catalog.toml, model.toml, creator.toml, sample.toml, or *.sample.toml")

            # Look for creator.toml
            if "creator.toml" in files:
                creator_data = self.process_creator(root_path)
                if creator_data:
                    creators.append(creator_data)

            # Look for .safetensors to identify a Model
            safetensors = [f for f in files if f.endswith(".safetensors")]
            if safetensors:
                print(f"  Found Model at: {root_path}")
                model_data = self.process_model(root_path, safetensors, catalog)
                if model_data:
                    models.append(model_data)
        
        # Auto-generate creators from models that don't have a creator.toml
        known_creators = {c["manifest"].name or c["manifest"].title for c in creators if c["manifest"]}
        for m in models:
            c_name = m.get("display_creator")
            if c_name and c_name not in known_creators and c_name != (getattr(catalog, "creator", None) if catalog else None):
                c_manifest = CreatorManifest(title=c_name)
                creators.append({
                    "manifest": c_manifest,
                    "dir": self.catalog_dir / str(c_name)
                })
                known_creators.add(c_name)

        # 7. Generate Search Data
        search_data = self._prepare_search_data(catalog, models, creators)
        import json
        with open(self.site_dir / "search_data.json", "w", encoding="utf-8") as f:
            json.dump(search_data, f, indent=2)

        # 8. Render Index
        self.render_index(catalog, models, search_data)

        # 9. Render Creator pages
        for creator_data in creators:
            self.render_creator_page(creator_data, catalog, models, search_data)

        # 10. Generate Feeds (Atom + RSS)
        base_url = getattr(catalog, "base_url", None) or ""
        if base_url and catalog and catalog.feeds is not False:
            generate_atom_feed(catalog, models, base_url, self.site_dir / "feed.atom")
            generate_rss_feed(catalog, models, base_url, self.site_dir / "feed.rss")
        elif base_url and catalog and catalog.feeds is False:
            print("  Skipping feed generation: disabled in catalog.toml")
        else:
            print("  Skipping feed generation: no base_url set in catalog.toml")
        
        print("Build complete!")

    def process_model(self, model_dir: Path, safetensor_files: List[str], catalog: Optional[CatalogManifest]):
        manifest_path = model_dir / "model.toml"
        if manifest_path.exists():
            data = load_toml(manifest_path)
            errors = validate_manifest("model.toml", data)
            if errors:
                print(f"Validation errors in {manifest_path}:")
                for key, err in errors.items():
                    print(f"  - {key}: {err}")
                return None
            model_manifest = parse_model(manifest_path)
            
            # Default missing creator to parent directory if nested
            if not model_manifest.creator and not model_manifest.creators:
                if model_dir.parent != self.catalog_dir:
                    model_manifest.creator = model_dir.parent.name

            # Resolve creator via aliases if present
            if model_manifest.creator and model_manifest.creator in self.creator_aliases:
                model_manifest.creator = self.creator_aliases[model_manifest.creator]
        else:
            implicit_creator = model_dir.parent.name if model_dir.parent != self.catalog_dir else None
            model_manifest = ModelManifest(title=model_dir.name, creator=implicit_creator)
            
        try:
            rel_path = model_dir.relative_to(self.catalog_dir)
            if model_manifest.permalink:
                if str(rel_path.parent) == ".":
                    model_slug = model_manifest.permalink
                else:
                    model_slug = f"{str(rel_path.parent)}/{model_manifest.permalink}"
            else:
                model_slug = str(rel_path)
        except ValueError:
            model_slug = model_manifest.permalink or model_dir.name

        model_slug = model_slug.lower().replace(" ", "-")
        model_manifest.permalink = model_slug
        
        model_site_dir = self.site_dir / model_slug
        model_site_dir.mkdir(parents=True, exist_ok=True)

        # 1. Filename Validation & Stem Calculation
        generic_names = {"model", "lora", "weights", "base"}
        if len(safetensor_files) > 1:
            generic_stems = [Path(f).stem.lower() for f in safetensor_files]
            for s in generic_stems:
                if s in generic_names:
                    import sys
                    sys.exit(f"FATAL ERROR: Folder '{model_dir}' contains multiple models, one of which has a generic name '{s}.safetensors'. Please rename all models in this folder to be unique.")

        main_model_file = model_dir / safetensor_files[0]
        original_stem = main_model_file.stem
        
        # Determine model_stem (slug if generic, original if unique)
        if original_stem.lower() in generic_names:
            model_stem = model_slug.split('/')[-1]
        else:
            model_stem = original_stem

        # 2. Generate Metadata JSON
        metadata_filename = f"{model_stem}.metadata.json"
        meta_json = generate_metadata_json(model_manifest, main_model_file)
        save_metadata(meta_json, model_site_dir / metadata_filename)

        # 2. Handle Preview Image / Video
        preview_url = None
        video_url = None
        
        # Determine target preview format
        target_ext = model_manifest.preview_format or (catalog.preview_format if catalog else "jpg")
        target_ext = target_ext.lstrip(".").lower()
        if target_ext == "jpeg":
            target_ext = "jpg"
            
        image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        video_extensions = {".mp4"}
        gif_extensions = {".gif"}
        
        all_exts = image_extensions | video_extensions | gif_extensions
        
        target_preview = None
        
        # 1. Check if model.toml explicitly declares a preview file
        if model_manifest.preview:
            declared_file = model_dir / model_manifest.preview
            if declared_file.exists() and declared_file.suffix.lower() in all_exts:
                target_preview = declared_file
            else:
                print(f"  WARNING: Declared preview '{model_manifest.preview}' not found or invalid type.")
                
        # 2. Look for expected filenames (preview.* or cover.*)
        if not target_preview:
            for f in sorted(model_dir.iterdir()):
                if f.stem.lower() in ("cover", "preview") and f.suffix.lower() in all_exts:
                    target_preview = f
                    break
                    
        # 3. Fallback: grab the first valid image/video we find
        if not target_preview:
            for f in sorted(model_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in all_exts:
                    target_preview = f
                    break
        
        from .media import optimize_image, extract_poster_image
        import shutil
        
        if target_preview:
            f = target_preview
            ext = f.suffix.lower()
            
            if ext in video_extensions:
                # Video preview - copy and extract poster
                video_dest = model_site_dir / f"{model_stem}.preview{ext}"
                shutil.copy2(f, video_dest)
                video_url = video_dest.name
                
                # Extract poster as JPG (fallback/preview)
                poster_dest = model_site_dir / f"{model_stem}.preview.jpg"
                if extract_poster_image(f, poster_dest):
                    preview_url = poster_dest.name
                
            elif ext in gif_extensions:
                # Animated GIF - copy as-is, also extract a static poster for index card
                gif_dest = model_site_dir / f"{model_stem}.preview.gif"
                shutil.copy2(f, gif_dest)
                video_url = gif_dest.name  # Reuse video_url for animated display
                
                # Extract static frame for catalog card using Pillow
                poster_dest = model_site_dir / f"{model_stem}.preview.jpg"
                try:
                    from PIL import Image
                    with Image.open(f) as img:
                        img.seek(0)  # First frame
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        img.thumbnail((800, 800))
                        img.save(poster_dest, "JPEG", quality=85, optimize=True)
                    preview_url = poster_dest.name
                except Exception as e:
                    print(f"  GIF poster extraction error: {e}")
                
            elif ext in image_extensions:
                # Image preview
                preview_dest = model_site_dir / f"{model_stem}.preview.{target_ext}"
                if optimize_image(f, preview_dest, format=target_ext):
                    preview_url = preview_dest.name
        else:
            print(f"  WARNING: No preview images found for {model_dir.name}. Using default placeholder.")
            # Use __file__ to resolve the package directory reliably
            pkg_dir = Path(__file__).parent
            placeholder_src = pkg_dir / "static" / "placeholder.jpg"
            if placeholder_src.exists():
                preview_dest = model_site_dir / f"{model_stem}.preview.jpg"
                shutil.copy2(placeholder_src, preview_dest)
                preview_url = preview_dest.name
            else:
                print(f"  WARNING: Default placeholder missing from {placeholder_src}")
        
        # 3. Handle Asset Placement (Local vs CDN)
        model_filename = f"{model_stem}.safetensors"
        
        cdn_url = self.cdn_url  # local var so Pyre2 can narrow Optional[str]
        if cdn_url:
            # Split mode
            model_asset_path = Path(model_slug) / model_filename
            dest_asset = self.asset_dir / model_asset_path
            dest_asset.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(main_model_file, dest_asset)
            assert self.cdn_url is not None
            model_url = f"{cdn_url.rstrip('/')}/{model_asset_path}"
        else:
            # Combined mode
            dest_path = model_site_dir / model_filename
            import shutil
            shutil.copy2(main_model_file, dest_path)
            model_url = model_filename

        # 3. Discover Samples
        samples = []
        audio_extensions = {".mp3", ".wav", ".flac", ".opus"}
        image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        model_audio_files = []
        
        # Check for any audio files recursively (or just in main/samples) to determine if it's an image lora
        has_audio = False
        for root, _, files in os.walk(model_dir):
            if any(Path(f).suffix.lower() in audio_extensions for f in files):
                has_audio = True
                break
        
        is_image_lora = not has_audio
        
        if not is_image_lora:
            # Traditional Audio Lora processing
            # Check main model dir
            for f in model_dir.iterdir():
                if f.is_file() and f.suffix.lower() in audio_extensions:
                    sample_data = self.process_sample(f, model_slug, model_manifest)
                    if sample_data:
                        samples.append(sample_data)
                        model_audio_files.append(f)
                        
            # Check samples/ nested folder
            samples_dir = model_dir / "samples"
            if samples_dir.exists() and samples_dir.is_dir():
                for f in samples_dir.iterdir():
                    if f.is_file() and f.suffix.lower() in audio_extensions:
                        sample_data = self.process_sample(f, model_slug, model_manifest)
                        if sample_data:
                            samples.append(sample_data)
                            model_audio_files.append(f)
        else:
            # Image Lora processing - discover image files as samples recursively
            print(f"  Detected Image Lora (no audio found)")
            from .media import extract_image_metadata
            
            # Start with the main preview image if it exists
            discovered_images = []
            if target_preview:
                discovered_images.append(target_preview)

            # Discover all other images recursively
            for root, _, files in os.walk(model_dir):
                root_path = Path(root)
                # Skip samples/ if we already handled it? No, os.walk handles everything.
                # However, we want a consistent sorting.
                for f_name in sorted(files):
                    f = root_path / f_name
                    if f.suffix.lower() in image_extensions:
                        # Skip if it's already the target_preview or looks like a cover
                        if target_preview and f.resolve() == target_preview.resolve():
                            continue
                        if f.stem.lower() in ("cover", "preview"):
                            continue
                        if f_name.startswith("."):
                            continue
                        
                        discovered_images.append(f)
            
            # Process and copy images
            for img_path in discovered_images:
                # Extract metadata
                img_metadata = extract_image_metadata(img_path)
                
                # For images in subdirectories, we'll flatten them but avoid name collisions
                # by using a hash or relative path string if necessary.
                # For now, let's keep it simple and just use the filename, 
                # but maybe with a prefix if it's in a subfolder.
                try:
                    rel_to_model = img_path.relative_to(model_dir)
                    parts = list(rel_to_model.parts)
                    if parts[0] == "samples":
                        parts = parts[1:]
                    
                    if len(parts) > 1:
                        # e.g. subdir/img.png -> subdir_img.png
                        safe_name = "_".join(parts)
                    else:
                        safe_name = parts[0]
                except (ValueError, IndexError):
                    safe_name = img_path.name

                dest = model_site_dir / safe_name
                import shutil
                shutil.copy2(img_path, dest)
                
                # Mock a SampleManifest for the template's logic
                from .manifests import SampleManifest
                s_manifest = SampleManifest()
                
                # Populate if metadata found
                prompt_data = img_metadata.get("prompt", {})
                if isinstance(prompt_data, dict):
                    # Similar logic to process_sample's extraction
                    for node_id, node in prompt_data.items():
                        if isinstance(node, dict) and "class_type" in node:
                            inputs = node.get("inputs", {})
                            if not s_manifest.prompt and "text" in inputs and isinstance(inputs["text"], str):
                                s_manifest.prompt = inputs["text"]
                            if not s_manifest.seed and "seed" in inputs and isinstance(inputs["seed"], (int, float)):
                                s_manifest.seed = int(inputs["seed"])
                            if not s_manifest.steps and "steps" in inputs and isinstance(inputs["steps"], (int, float)):
                                s_manifest.steps = int(inputs["steps"])
                            if not s_manifest.cfg and "cfg" in inputs and isinstance(inputs["cfg"], (int, float)):
                                s_manifest.cfg = float(inputs["cfg"])
                            if not s_manifest.sampler and "sampler_name" in inputs:
                                s_manifest.sampler = inputs["sampler_name"]
                            if not s_manifest.scheduler and "scheduler" in inputs:
                                s_manifest.scheduler = inputs["scheduler"]
                
                from dataclasses import asdict
                samples.append({
                    "name": img_path.stem,
                    "url": safe_name,
                    "is_image": True,
                    "manifest": asdict(s_manifest),
                    "original_path": img_path
                })

        # 4. Discover Extras (Automatic + Manifest)
        extras = []
        ignored_extensions = {".toml", ".safetensors", ".mp3", ".wav", ".flac", ".opus", ".zip"}
        ignored_names = {"preview", "cover"}
        for f in model_dir.iterdir():
            if f.is_file():
                if f.suffix.lower() in ignored_extensions:
                    continue
                if f.stem.lower() in ignored_names:
                    continue
                if f.name.startswith("."):
                    continue
                if target_preview and f == target_preview:
                    continue
                extras.append(f)
        
        # Add explicit extras from manifest if they exist and haven't been added
        for extra_name in model_manifest.extras:
            extra_file = model_dir / extra_name
            if extra_file.exists() and extra_file not in extras:
                extras.append(extra_file)

        # 5. Prepare Download Links (Replaced ZIP bundling)
        downloads: List[Dict[str, Any]] = [
            {"label": "Model", "title": "Download Model", "url": model_url, "is_zip": False, "primary": True},
            {"label": "Metadata", "title": "Download Metadata", "url": metadata_filename, "is_zip": False, "primary": False}
        ]
        
        if is_image_lora and target_preview:
            # For image loras, download the ORIGINAL preview image as requested
            preview_filename = f"{model_stem}.preview{target_preview.suffix.lower()}"
            downloads.append({
                "label": "Preview Art", 
                "title": f"Download Preview Art ({preview_filename})", 
                "url": preview_url, 
                "is_zip": False, 
                "primary": False
            })
        elif preview_url:
            downloads.append({"label": "Preview Art", "title": f"Download Preview Art ({preview_url})", "url": preview_url, "is_zip": False, "primary": False})
            
        if video_url:
            downloads.append({"label": "Preview Video", "title": "Download Preview Video", "url": video_url, "is_zip": False, "primary": False})

        for extra_f in extras:
            # Copy extras to output for individual download
            extra_dest = model_site_dir / extra_f.name
            import shutil
            shutil.copy2(extra_f, extra_dest)
            downloads.append({
                "label": extra_f.name, 
                "title": f"Download Extra: {extra_f.name}", 
                "url": extra_f.name, 
                "is_zip": False, 
                "primary": False
            })

        # 6. Prepare Search Data
        # (This is now handled at the end of run() and passed back during re-rendering if needed, 
        # but for individual model pages we might need it passed in)
        
        # 7. Render Detail Page
        self.render_model_page(model_manifest, samples, model_url, preview_url, video_url, downloads, model_site_dir, catalog=catalog, is_image_lora=is_image_lora)

        # Build list of creators for the index
        display_creator = model_manifest.creator
        if not display_creator and model_manifest.creators:
            display_creator = ", ".join(model_manifest.creators)
        elif not display_creator and catalog:
            display_creator = getattr(catalog, "creator", None)

        return {
            "manifest": model_manifest,
            "model_url": model_url,
            "preview_url": preview_url,
            "video_url": video_url,
            "display_creator": display_creator,
            "dir": model_dir,
            "slug": model_slug,
            "samples": samples,
            "is_image_lora": is_image_lora
        }

    def process_sample(self, audio_file: Path, model_slug: str, model_manifest: ModelManifest):
        from .media import transcode_audio, get_audio_duration, extract_mp3_metadata
        import json
        
        # Look for sample manifest in order of priority:
        # 1. <filename>.sample.toml
        # 2. <filename>.toml
        # 3. sample.toml (if in a subfolder)
        candidates = [
            audio_file.parent / (audio_file.stem + ".sample.toml"),
            audio_file.with_suffix(".toml"),
            audio_file.parent / "sample.toml"
        ]
        
        manifest_path = None
        for cand in candidates:
            if cand.exists():
                manifest_path = cand
                break
                
        sample_manifest = None
        if manifest_path:
            data = load_toml(manifest_path)
            errors = validate_manifest("sample.toml", data)
            if errors:
                print(f"Validation errors in {manifest_path}:")
                for key, err in errors.items():
                    print(f"  - {key}: {err}")
                return None
            sample_manifest = parse_sample(manifest_path)
        else:
            sample_manifest = SampleManifest()
            
        # Extract MP3 metadata before transcoding
        mp3_meta = extract_mp3_metadata(audio_file)
        
        # Populate manifest with extracted data if not explicitly set
        if mp3_meta:
            # 1. Standard ID3 tags — used as gentle fallbacks
            id3_tags = mp3_meta.get("tags", {})
            if not sample_manifest.title and id3_tags.get("title"):
                sample_manifest.title = id3_tags["title"]
            if not sample_manifest.creator and id3_tags.get("artist"):
                sample_manifest.creator = id3_tags["artist"]
            if not sample_manifest.bpm and id3_tags.get("bpm"):
                sample_manifest.bpm = float(id3_tags["bpm"])
            if not sample_manifest.lyrics and id3_tags.get("lyrics"):
                sample_manifest.lyrics = id3_tags["lyrics"]

            # 2. ComfyUI TXXX:prompt — extract fields from the workflow graph
            prompt_data = mp3_meta.get("prompt", {})
            if isinstance(prompt_data, dict):
                # Try to find standard comfyui Audio/Video nodes that might contain text
                # This is highly specific to the ComfyUI workflow format, but we'll extract
                # what we can. For robust support, the user can still use sample.toml.
                # A common pattern is finding a TextEncode node.
                for node_id, node in prompt_data.items():
                    if isinstance(node, dict) and "class_type" in node:
                        ctype = node["class_type"]
                        if "inputs" in node:
                            inputs = node["inputs"]
                            # Try to extract common fields if sample_manifest lacks them
                            if not sample_manifest.prompt and "text" in inputs and isinstance(inputs["text"], str):
                                sample_manifest.prompt = inputs["text"]
                            if not sample_manifest.prompt and "tags" in inputs and isinstance(inputs["tags"], str):
                                sample_manifest.prompt = inputs["tags"]
                            if not sample_manifest.lyrics and "lyrics" in inputs and isinstance(inputs["lyrics"], str):
                                sample_manifest.lyrics = inputs["lyrics"]
                            if not sample_manifest.seed and "seed" in inputs and isinstance(inputs["seed"], (int, float)):
                                sample_manifest.seed = int(inputs["seed"])
                            if not sample_manifest.bpm and "bpm" in inputs and isinstance(inputs["bpm"], (int, float)):
                                sample_manifest.bpm = float(inputs["bpm"])
            elif isinstance(prompt_data, str) and not sample_manifest.prompt:
                 sample_manifest.prompt = prompt_data
        
        # Output to SLUG/samples/filename.opus
        if self.cdn_url:
            sample_asset_path = Path(model_slug) / "samples"
            sample_asset_path = sample_asset_path / (audio_file.stem + ".opus")
            dest_asset = self.asset_dir / sample_asset_path
            dest_asset.parent.mkdir(parents=True, exist_ok=True)
            transcode_dest = dest_asset
        else:
            sample_rel_dir = Path("samples")
            dest_dir = self.site_dir / model_slug / sample_rel_dir
            dest_dir.mkdir(parents=True, exist_ok=True)
            transcode_dest = dest_dir / (audio_file.stem + ".opus")

        print(f"  Transcoding sample: {audio_file.name} -> {transcode_dest.name}")
        
        # Use manifest metadata if available
        sample_title = audio_file.stem
        sample_creator = model_manifest.creator
        if sample_manifest:
            if sample_manifest.title:
                sample_title = sample_manifest.title
            if sample_manifest.creator:
                sample_creator = sample_manifest.creator

        transcode_audio(audio_file, transcode_dest, title=sample_title, creator=sample_creator)
        
        # Save workflow JSON next to the transcoded audio if present
        workflow_url = None
        if "workflow" in mp3_meta:
            workflow_dest = transcode_dest.with_suffix(".workflow.json")
            with open(workflow_dest, "w", encoding="utf-8") as wf:
                json.dump(mp3_meta["workflow"], wf, indent=2)
            workflow_url = workflow_dest.name
            print(f"  Extracted workflow -> {workflow_dest.name}")
        
        duration = get_audio_duration(transcode_dest)
        
        cdn_url = self.cdn_url  # local var so Pyre2 can narrow Optional[str]
        if cdn_url:
            sample_url = f"{cdn_url.rstrip('/')}/{sample_asset_path}"
            if workflow_url:
                workflow_url = f"{cdn_url.rstrip('/')}/{sample_asset_path.parent}/{workflow_url}"
        else:
            sample_url = f"samples/{transcode_dest.name}"
            if workflow_url:
                workflow_url = f"samples/{Path(workflow_url).name}"
        
        # Discover per-sample cover art
        cover_url = None
        image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        sample_dir = audio_file.parent
        
        # 1. Explicit cover field in sample manifest
        if sample_manifest and sample_manifest.cover:
            cover_file = sample_dir / sample_manifest.cover
            if cover_file.exists():
                cover_url = self._copy_sample_cover(cover_file, model_slug, audio_file.stem)
            else:
                cover_url = self._copy_sample_cover(None, model_slug, audio_file.stem, label=f"Sample cover '{sample_manifest.cover}'")
        
        # 2. Same-stem image (e.g. demo_1.jpg for demo_1.mp3)
        if not cover_url:
            for ext in image_extensions:
                candidate = audio_file.with_suffix(ext)
                if candidate.exists():
                    cover_url = self._copy_sample_cover(candidate, model_slug, audio_file.stem)
                    break
        
        # 3. preview.* or cover.* in the same directory
        if not cover_url:
            for f in sorted(sample_dir.iterdir()):
                if f.is_file() and f.stem.lower() in ("cover", "preview") and f.suffix.lower() in image_extensions:
                    cover_url = self._copy_sample_cover(f, model_slug, audio_file.stem)
                    break

        from dataclasses import asdict
        return {
            "name": sample_title,
            "url": sample_url,
            "duration": duration,
            "manifest": asdict(sample_manifest) if sample_manifest else None,
            "workflow_url": workflow_url,
            "cover_url": cover_url,
            "external_page": sample_manifest.external_page if sample_manifest else None,
        }

    def _verify_asset(self, src: Optional[Path], dest: Path, label: str = "Asset") -> bool:
        """
        Verify that an asset exists, copy it to dest, and issue warnings if missing.
        Returns True if successful, False if missing.
        If missing and it's an image-like destination, copies a default placeholder.
        """
        import shutil
        if src and src.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            return True
        else:
            if src:
                print(f"  [WARNING] Missing {label}: {src}")
            else:
                print(f"  [WARNING] Missing {label} (not specified or invalid)")
                
            # Fallback for images
            if dest.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
                placeholder_src = Path(__file__).parent / "static" / "img" / "missing.png"
                if placeholder_src.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(placeholder_src, dest)
                    return True
            return False

    def _copy_sample_cover(self, cover_file: Optional[Path], model_slug: str, sample_stem: str, label: str = "Sample cover") -> Optional[str]:
        """Copy a sample cover image to the output and return its URL relative to the model page."""
        dest_name = f"{sample_stem}_cover{cover_file.suffix.lower() if cover_file else '.png'}"
        if self.cdn_url:
            dest = self.asset_dir / model_slug / "samples" / dest_name
        else:
            dest = self.site_dir / model_slug / "samples" / dest_name
        
        self._verify_asset(cover_file, dest, label=label)
        
        cdn_url = self.cdn_url
        if cdn_url:
            return f"{cdn_url.rstrip('/')}/{model_slug}/samples/{dest_name}"
        return f"samples/{dest_name}"

    def render_model_page(self, model_manifest: ModelManifest, samples: List[Dict], model_url: str, preview_url: Optional[str], video_url: Optional[str], downloads: List[Dict], output_dir: Path, catalog: Optional[CatalogManifest] = None, search_data: Optional[Dict] = None, is_image_lora: bool = False):
        try:
            template = self.env.get_template("model.html")
        except Exception:
            return

        base_url = getattr(catalog, "base_url", None) or ""
        model_slug = output_dir.name
        og_custom = model_manifest.opengraph if isinstance(model_manifest.opengraph, dict) else {}
        og_title = og_custom.get("title") or model_manifest.title
        og_description = og_custom.get("description") or model_manifest.synopsis or (model_manifest.about or "")[:256]
        
        if og_custom.get("image") and base_url:
            og_image = f"{base_url}/{model_slug}/{og_custom['image'].lstrip('/')}"
        else:
            og_image = f"{base_url}/{model_slug}/{preview_url}" if base_url and preview_url else ""
            
        try:
            rel_path = output_dir.relative_to(self.site_dir)
            depth = len(rel_path.parts)
        except ValueError:
            depth = 1
        computed_relative_root = "../" * depth if depth > 0 else "./"
            
        content = template.render(
            model=model_manifest,
            samples=samples,
            model_url=model_url,
            preview_url=preview_url,
            video_url=video_url,
            downloads=downloads,
            catalog=catalog,
            base_url=base_url,
            relative_root=computed_relative_root,
            theme_css=self.theme_css,
            og_title=og_title,
            og_description=og_description,
            og_image=og_image,
            og_url=f"{base_url}/{model_slug}/" if base_url else "",
            og_type="article",
            is_index=False,
            search_data=None, # Don't embed on subpages
            is_image_lora=is_image_lora,
            build_id=self.build_id,
            debug_layout=self.debug_layout,
        )
        with open(output_dir / "index.html", "w") as f:
            f.write(content)

    def render_index(self, catalog: Optional[CatalogManifest], models: List[Dict], search_data: Optional[Dict] = None):
        template = self.env.get_template("index.html")
        base_url = getattr(catalog, "base_url", None) or ""
        
        og_custom = catalog.opengraph if catalog and isinstance(catalog.opengraph, dict) else {}
        og_title = og_custom.get("title") or getattr(catalog, "title", None)
        og_description = og_custom.get("description") or getattr(catalog, "synopsis", None)
        
        og_image = ""
        if og_custom.get("image") and base_url:
            og_image = f"{base_url}/{og_custom['image'].lstrip('/')}"
        elif models and models[0].get("preview_url"):
            first_slug = models[0].get("slug", "")
            og_image = f"{base_url}/{first_slug}/{models[0]['preview_url']}" if base_url else ""
            
        content = template.render(
            catalog=catalog,
            models=models,
            base_url=base_url,
            relative_root="./",
            theme_css=self.theme_css,
            og_title=og_title,
            og_description=og_description,
            og_image=og_image,
            og_url=base_url + "/" if base_url else "",
            og_type="website",
            is_index=True,
            search_data=search_data,
            build_id=self.build_id,
            debug_layout=self.debug_layout,
        )
        with open(self.site_dir / "index.html", "w") as f:
            f.write(content)

    def render_creator_page(self, creator_data: Dict, catalog: Optional[CatalogManifest], all_models: List[Dict], search_data: Optional[Dict] = None):
        """Render a creator's own page with their profile and model list."""
        if not creator_data:
            return
        manifest = creator_data.get("manifest")
        if not manifest:
            return

        # If a permalink is explicitly set, use it. Try to compute from dir otherwise.
        creator_slug = manifest.permalink
        if not creator_slug:
            creator_dir = creator_data.get("dir")
            if creator_dir and creator_dir != self.catalog_dir:
                try:
                    rel_path = creator_dir.relative_to(self.catalog_dir)
                    creator_slug = str(rel_path)
                except ValueError:
                    creator_slug = creator_dir.name
            else:
                creator_slug = manifest.name or manifest.title or "creator"
                
        creator_slug = creator_slug.lower().replace(" ", "-")
        manifest.permalink = creator_slug
        
        creator_site_dir = self.site_dir / creator_slug
        creator_site_dir.mkdir(parents=True, exist_ok=True)

        # Find models by this creator
        creator_name = manifest.name or manifest.title
        creator_models = [
            m for m in all_models
            if creator_name and (
                (m.get("manifest") and m["manifest"].creator == creator_name)
                or (m.get("manifest") and creator_name in (m["manifest"].creators or []))
            )
        ]

        # Handle creator image if specified
        creator_image_url = None
        if manifest.image:
            # Check for a specific 'profile.png' as hinted by user request
            src = creator_data["dir"] / manifest.image
            dest = creator_site_dir / manifest.image
            if self._verify_asset(src, dest, label=f"Creator profile image '{manifest.image}'"):
                creator_image_url = manifest.image
            else:
                # If verify_asset used fallback, the file exists now at dest
                creator_image_url = manifest.image

        base_url = getattr(catalog, "base_url", None) or ""
        
        # Check for external_page redirect
        external_url = None
        for link in manifest.links: # Assuming manifest.links is a list of dicts
            if isinstance(link, dict) and "external_page" in link:
                external_url = link["external_page"]
                break
        
        if external_url:
            # Generate a simple redirect page instead of the full creator page
            template = self.env.from_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={{ url }}">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="{{ url }}">{{ url }}</a></p>
</body>
</html>''')
            content = template.render(url=external_url)
        else:
            try:
                template = self.env.get_template("creator.html")
            except Exception:
                return
            og_custom = manifest.opengraph if isinstance(manifest.opengraph, dict) else {}
            og_title = og_custom.get("title") or creator_name
            og_description = og_custom.get("description") or getattr(manifest, "synopsis", None)
            
            if og_custom.get("image") and base_url:
                og_image = f"{base_url}/{creator_slug}/{og_custom['image'].lstrip('/')}"
            else:
                og_image = f"{base_url}/{creator_slug}/{creator_image_url}" if base_url and creator_image_url else ""
                
            try:
                rel_path = creator_site_dir.relative_to(self.site_dir)
                depth = len(rel_path.parts)
            except ValueError:
                depth = 1
            computed_relative_root = "../" * depth if depth > 0 else "./"
                
            content = template.render(
                catalog=catalog,
                creator=manifest,
                models=creator_models,
                creator_image_url=creator_image_url,
                base_url=base_url,
                relative_root=computed_relative_root,
                theme_css=self.theme_css,
                og_title=og_title,
                og_description=og_description,
                og_image=og_image,
                og_url=f"{base_url}/{creator_slug}/" if base_url else "",
                og_type="profile",
                is_index=False,
                search_data=None, # Don't embed on subpages
                build_id=self.build_id,
                debug_layout=self.debug_layout,
            )
        with open(creator_site_dir / "index.html", "w") as f:
            f.write(content)
        print(f"  Creator page: /{creator_slug}/")

    def _prepare_search_data(self, catalog: Optional[CatalogManifest], models: List[Dict], creators: List[Dict]) -> Dict:
        """Prepare a JSON-serializable structure for the frontend search."""
        search_models = []
        for m in models:
            m_manifest = m["manifest"]
            m_slug = m["slug"]
            
            search_model = {
                "title": m_manifest.title or m_slug,
                "url": f"{m_slug}/",
                "cover": m.get("preview_url") or "",
                "creator": m.get("display_creator") or "",
                "tags": getattr(m_manifest, "tags", []) or [],
                "tracks": []
            }
            
            # Since m["manifest"] might not have samples (they are discovered by engine),
            # we should really be getting the samples from somewhere.
            # In run(), after processing each model, we have the model data.
            # However, my run() loop doesn't store the samples in the 'models' list yet.
            # Let's check process_model again.
            
            # Actually, process_model doesn't return samples in its results dict.
            # I should fix that first or find another way.
            
            # Re-evaluating: I'll update process_model to return samples.
            if "samples" in m:
                for i, s in enumerate(m["samples"]):
                    s_manifest = s.get("manifest")
                    s_tags = []
                    if s_manifest:
                        if isinstance(s_manifest, dict):
                            s_tags = s_manifest.get("tags", [])
                        else:
                            s_tags = getattr(s_manifest, "tags", [])
                    
                    search_model["tracks"].append({
                        "title": s["name"],
                        "url": f"{m_slug}/",
                        "cover": s.get("cover_url") or "",
                        "tags": s_tags or [],
                        "number": str(i + 1)
                    })
            
            search_models.append(search_model)
            
        search_creators = []
        for c in creators:
            c_manifest = c["manifest"]
            # Compute slug similar to render_creator_page
            c_slug = c_manifest.permalink
            if not c_slug:
                c_dir = c.get("dir")
                if c_dir and c_dir != self.catalog_dir:
                    try:
                        rel_path = c_dir.relative_to(self.catalog_dir)
                        c_slug = str(rel_path)
                    except ValueError:
                        c_slug = c_dir.name
                else:
                    c_slug = c_manifest.name or c_manifest.title or "creator"
            
            c_slug = c_slug.lower().replace(" ", "-")
            
            search_creators.append({
                "name": c_manifest.name or c_manifest.title,
                "url": f"{c_slug}/",
                "image": getattr(c_manifest, "image", "") or ""
            })
            
        return {
            "models": search_models,
            "creators": search_creators
        }

    def process_creator(self, creator_dir: Path):
        manifest_path = creator_dir / "creator.toml"
        data = load_toml(manifest_path)
        errors = validate_manifest("creator.toml", data)
        if errors:
            print(f"Validation errors in {manifest_path}:")
            for key, err in errors.items():
                print(f"  - {key}: {err}")
            return None
        
        creator_manifest = parse_creator(manifest_path)
        
        # Populate alias mapping
        canonical_name = creator_manifest.name or creator_dir.name
        if creator_manifest.aliases: # Ensure aliases exist before iterating
            for alias in creator_manifest.aliases:
                self.creator_aliases[alias] = canonical_name
            
        # The permalink defaults to the directory name if not specified
        return {
            "manifest": creator_manifest,
            "dir": creator_dir
        }
