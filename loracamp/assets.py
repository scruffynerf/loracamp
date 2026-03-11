import shutil
from pathlib import Path

def copy_static_assets(output_dir: Path):
    """
    Copy internal static assets to the build directory.
    Initially handles the minimalist site.css.
    """
    static_src = Path(__file__).parent / "static"
    static_dest = output_dir / "static"
    
    if static_src.exists():
        if static_dest.exists():
            shutil.rmtree(static_dest)
        shutil.copytree(static_src, static_dest)

def handle_custom_assets(custom_paths: list, output_dir: Path):
    """
    Copy user-provided custom assets to the build directory.
    """
    for path_str in custom_paths:
        path = Path(path_str)
        if path.exists():
            dest = output_dir / path.name
            if path.is_dir():
                shutil.copytree(path, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(path, dest)
