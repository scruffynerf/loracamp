import pytest
from pathlib import Path
from PIL import Image
from loracamp.media import optimize_image

def test_optimize_image_square_padding(tmp_path):
    """Test that optimize_image adds square padding correctly."""
    # 1. Wide image (2:1)
    wide_img = tmp_path / "wide.png"
    with Image.new("RGB", (200, 100), color="red") as img:
        wide_img_path = str(wide_img)
        img.save(wide_img_path)
    
    wide_out = tmp_path / "wide_out.png"
    result = optimize_image(wide_img, wide_out, format="png", max_size=100)
    assert result is True
    assert wide_out.exists()
    
    with Image.open(wide_out) as img:
        assert img.size == (100, 100)
        # Check that it's letterboxed (red in middle, black on top/bottom)
        # Wait, wide image (200x100) -> resized to (100x50) -> padded to (100x100)
        # So it should have black bars on TOP and BOTTOM.
        assert img.getpixel((50, 0)) == (0, 0, 0) # Top bar
        assert img.getpixel((50, 50)) == (255, 0, 0) # Red content
        assert img.getpixel((50, 99)) == (0, 0, 0) # Bottom bar

def test_optimize_image_tall_padding(tmp_path):
    """Test that optimize_image adds pillarboxing for tall images."""
    # 2. Tall image (1:2)
    tall_img = tmp_path / "tall.png"
    with Image.new("RGB", (100, 200), color="blue") as img:
        img.save(tall_img)
    
    tall_out = tmp_path / "tall_out.png"
    result = optimize_image(tall_img, tall_out, format="png", max_size=100)
    assert result is True
    
    with Image.open(tall_out) as img:
        assert img.size == (100, 100)
        # Check pillarboxing (blue in middle, black on left/right)
        assert img.getpixel((0, 50)) == (0, 0, 0) # Left bar
        assert img.getpixel((50, 50)) == (0, 0, 255) # Blue content
        assert img.getpixel((99, 50)) == (0, 0, 0) # Right bar

def test_optimize_image_already_square(tmp_path):
    """Test that square images are resized without unnecessary padding."""
    sq_img = tmp_path / "sq.png"
    with Image.new("RGB", (300, 300), color=(0, 255, 0)) as img:
        img.save(sq_img)
    
    sq_out = tmp_path / "sq_out.png"
    optimize_image(sq_img, sq_out, format="png", max_size=100)
    
    with Image.open(sq_out) as img:
        assert img.size == (100, 100)
        assert img.getpixel((0, 0)) == (0, 255, 0)
