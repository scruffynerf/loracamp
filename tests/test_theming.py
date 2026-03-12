import pytest
from loracamp.theming import generate_theme_css, _dark_palette, _light_palette

def test_generate_theme_css_default():
    css = generate_theme_css(None)
    assert "<style>" in css
    assert ":root" in css
    assert "--bg-1" in css
    assert "--cover-border-radius: 0;" in css

def test_generate_theme_css_light_mode():
    theme = {"base": "light", "accent_hue": 0, "accent_chroma": 50, "round_corners": True}
    css = generate_theme_css(theme)
    assert "--cover-border-radius: 0.4rem;" in css
    # Light palette generates specific lightness values
    assert "hsl(0, 5%, 97%)" in css

def test_generate_theme_css_dark_mode():
    theme = {"base": "dark", "accent_hue": 210, "accent_chroma": 40}
    css = generate_theme_css(theme)
    assert "hsl(210, 4%, 10%)" in css  # --bg-1 for dark mode with hue 210, chroma 40 -> cs = 0.4 -> 4%

def test_dark_palette():
    palette = _dark_palette(200, 100) # cs = 1.0 -> 10% saturation for bg-1
    assert palette["--bg-1"] == "hsl(200, 10%, 10%)"

def test_light_palette():
    palette = _light_palette(100, 10)  # cs = 0.1 -> 1% saturation for bg-1
    assert palette["--bg-1"] == "hsl(100, 1%, 97%)"
