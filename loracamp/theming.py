"""
Generate CSS custom properties from a catalog's [theme] config.

Faircamp-compatible color scheme: derives all needed CSS variables from
a base mode (dark/light), an accent hue, and an accent chroma value.
"""
from typing import Dict, Any, Optional


def generate_theme_css(theme: Optional[Dict[str, Any]]) -> str:
    """Return a <style> block string with :root CSS custom properties."""
    if theme is None:
        theme = {}

    base = theme.get("base", "dark")
    accent_hue = theme.get("accent_hue", 210)
    accent_chroma = theme.get("accent_chroma", 40)
    round_corners = theme.get("round_corners", False)

    if base == "light":
        css_vars = _light_palette(accent_hue, accent_chroma)
    else:
        css_vars = _dark_palette(accent_hue, accent_chroma)

    css_vars["--cover-border-radius"] = "0.4rem" if round_corners else "0"
    css_vars["--ul-list-style-type"] = "disc"

    lines = [f"    {k}: {v};" for k, v in css_vars.items()]
    return "<style>\n:root {\n" + "\n".join(lines) + "\n}\n</style>"


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
