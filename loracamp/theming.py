"""
Generate CSS custom properties from a catalog's [theme] config.

Faircamp-compatible color scheme: derives all needed CSS variables from
a base mode (dark/light), an accent hue, and an accent chroma value.
"""
from typing import Dict, Any, Optional, Callable


# Registry for theme palettes. 
# Key is the theme name (e.g., 'dark', 'light', 'ocean')
# Value is a callable that takes (hue, chroma) and returns a Dict[str, str]
PALETTE_REGISTRY: Dict[str, Callable[[int, int], Dict[str, str]]] = {}


def register_palette(name: str, func: Callable[[int, int], Dict[str, str]]):
    """Register a new color palette generator."""
    PALETTE_REGISTRY[name] = func


def generate_theme_css(theme: Optional[Dict[str, Any]]) -> str:
    """Return a <style> block string with :root CSS custom properties."""
    if theme is None:
        theme = {}

    accent_hue = theme.get("accent_hue", 210)
    accent_chroma = theme.get("accent_chroma", 40)
    round_corners = theme.get("round_corners", False)

    # Use registered palettes if available
    light_vars = PALETTE_REGISTRY.get("light", _light_palette)(accent_hue, accent_chroma)
    dark_vars = PALETTE_REGISTRY.get("dark", _dark_palette)(accent_hue, accent_chroma)

    # If a specific custom palette is requested as the 'base'
    base_name = theme.get("base", "dark")
    if base_name in PALETTE_REGISTRY and base_name not in ("light", "dark"):
        # We allow a custom named palette to override the base logic
        custom_vars = PALETTE_REGISTRY[base_name](accent_hue, accent_chroma)
        default_vars = custom_vars
    else:
        default_vars = light_vars if base_name == "light" else dark_vars

    # Shared variables
    shared_vars = {
        "--cover-border-radius": "0.4rem" if round_corners else "0",
        "--ul-list-style-type": "disc",
    }
    
    css_string = "<style>\n"
    
    # 1. Base Variables (Shared)
    css_string += ":root {\n"
    css_string += "\n".join([f"    {k}: {v};" for k, v in shared_vars.items()])
    css_string += "\n}\n\n"
    
    # 2. Default Theme (prefers-color-scheme fallback)
    css_string += ":root {\n"
    css_string += "\n".join([f"    {k}: {v};" for k, v in default_vars.items()])
    css_string += "\n}\n\n"
    
    # 3. Explicit Light/Dark overrides (forced via JS)
    css_string += ":root[data-theme=\"light\"] {\n"
    css_string += "\n".join([f"    {k}: {v};" for k, v in light_vars.items()])
    css_string += "\n}\n\n"
    
    css_string += ":root[data-theme=\"dark\"] {\n"
    css_string += "\n".join([f"    {k}: {v};" for k, v in dark_vars.items()])
    css_string += "\n}\n\n"
    
    # 4. OS-level prefers-color-scheme (if no explicit JS override)
    css_string += "@media (prefers-color-scheme: light) {\n"
    css_string += "    :root:not([data-theme=\"dark\"]) {\n"
    css_string += "\n".join([f"        {k}: {v};" for k, v in light_vars.items()])
    css_string += "\n    }\n"
    css_string += "}\n\n"
    
    css_string += "@media (prefers-color-scheme: dark) {\n"
    css_string += "    :root:not([data-theme=\"light\"]) {\n"
    css_string += "\n".join([f"        {k}: {v};" for k, v in dark_vars.items()])
    css_string += "\n    }\n"
    css_string += "}\n"
    
    css_string += "</style>"
    return css_string


def _dark_palette(hue: int, chroma: int) -> Dict[str, str]:
    h = hue
    c = chroma
    # Scale chroma to a 0-1 range for blending (input is 0-100ish)
    cs = min(c / 100, 1.0)

    return {
        "--bg-1":            f"hsl({h}, {int(cs*10)}%, 10%)",
        "--bg-1-90":         f"hsla({h}, {int(cs*10)}%, 10%, 0.9)",
        "--bg-1-overlay":    f"hsla({h}, {int(cs*10)}%, 10%, 0.85)",
        "--bg-2":            f"hsl({h}, {int(cs*10)}%, 16%)",
        "--bg-2-overlay":    f"hsla({h}, {int(cs*10)}%, 16%, 0.85)",
        "--bg-3":            f"hsl({h}, {int(cs*10)}%, 24%)",
        "--bg-mg":           f"hsl({h}, {int(cs*10)}%, 30%)",
        "--bg-acc":          f"hsl({h}, {int(cs*60)}%, 45%)",
        "--bg-acc-overlay":  f"hsla({h}, {int(cs*60)}%, 45%, 0.85)",
        "--mg":              f"hsl({h}, {int(cs*10)}%, 50%)",
        "--mg-acc":          f"hsl({h}, {int(cs*50)}%, 55%)",
        "--mg-acc-overlay":  f"hsla({h}, {int(cs*50)}%, 55%, 0.85)",
        "--fg-1":            f"hsl({h}, {int(cs*10)}%, 90%)",
        "--fg-1-focus":      f"hsl({h}, {int(cs*20)}%, 95%)",
        "--fg-1-veil":       f"hsla({h}, {int(cs*10)}%, 90%, 0.08)",
        "--fg-2":            f"hsl({h}, {int(cs*10)}%, 78%)",
        "--fg-3":            f"hsl({h}, {int(cs*10)}%, 65%)",
        "--fg-3-focus":      f"hsl({h}, {int(cs*15)}%, 75%)",
        "--fg-acc":          f"hsl({h}, {int(cs*10)}%, 95%)",
    }


def _light_palette(hue: int, chroma: int) -> Dict[str, str]:
    h = hue
    c = chroma
    cs = min(c / 100, 1.0)

    return {
        "--bg-1":            f"hsl({h}, {int(cs*10)}%, 97%)",
        "--bg-1-90":         f"hsla({h}, {int(cs*10)}%, 97%, 0.9)",
        "--bg-1-overlay":    f"hsla({h}, {int(cs*10)}%, 97%, 0.85)",
        "--bg-2":            f"hsl({h}, {int(cs*10)}%, 90%)",
        "--bg-2-overlay":    f"hsla({h}, {int(cs*10)}%, 90%, 0.85)",
        "--bg-3":            f"hsl({h}, {int(cs*10)}%, 82%)",
        "--bg-mg":           f"hsl({h}, {int(cs*10)}%, 74%)",
        "--bg-acc":          f"hsl({h}, {int(cs*60)}%, 50%)",
        "--bg-acc-overlay":  f"hsla({h}, {int(cs*60)}%, 50%, 0.85)",
        "--mg":              f"hsl({h}, {int(cs*10)}%, 55%)",
        "--mg-acc":          f"hsl({h}, {int(cs*50)}%, 45%)",
        "--mg-acc-overlay":  f"hsla({h}, {int(cs*50)}%, 45%, 0.85)",
        "--fg-1":            f"hsl({h}, {int(cs*10)}%, 15%)",
        "--fg-1-focus":      f"hsl({h}, {int(cs*20)}%, 10%)",
        "--fg-1-veil":       f"hsla({h}, {int(cs*10)}%, 15%, 0.08)",
        "--fg-2":            f"hsl({h}, {int(cs*10)}%, 28%)",
        "--fg-3":            f"hsl({h}, {int(cs*10)}%, 42%)",
        "--fg-3-focus":      f"hsl({h}, {int(cs*15)}%, 32%)",
        "--fg-acc":          f"hsl({h}, {int(cs*10)}%, 100%)",
    }


# Register default palettes
register_palette("dark", _dark_palette)
register_palette("light", _light_palette)
