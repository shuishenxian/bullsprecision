#!/usr/bin/env python3
"""
Image processing script for Bulls Precision website.
- Enhance main product images (contrast, sharpness, clean background)
- Generate themed thumbnail crops from available images
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os

IMG_DIR = os.path.dirname(os.path.abspath(__file__))

def enhance_product_image(input_path, output_path, bg_color=(245, 247, 250)):
    """Enhance product image: boost contrast/sharpness, clean up background."""
    img = Image.open(input_path)

    # Convert to RGBA for processing
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Resize to consistent size (max 800px width, maintain aspect)
    max_w = 800
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)

    # Convert back to RGB with clean background
    background = Image.new('RGB', img.size, bg_color)
    if img.mode == 'RGBA':
        background.paste(img, mask=img.split()[3])
    else:
        background.paste(img)
    img = background

    # Enhance contrast
    img = ImageEnhance.Contrast(img).enhance(1.15)
    # Enhance sharpness
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    # Slight brightness boost
    img = ImageEnhance.Brightness(img).enhance(1.05)

    # Save as high-quality JPEG
    img.save(output_path, 'JPEG', quality=92, optimize=True)
    print(f"  Enhanced: {os.path.basename(output_path)} ({img.width}x{img.height})")
    return img


def create_detail_crop(input_path, output_path, crop_region=None, size=(200, 200)):
    """Create a detail/closeup thumbnail from a region of the image."""
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    w, h = img.size
    if crop_region:
        # crop_region is (left_pct, top_pct, right_pct, bottom_pct) as 0-1
        box = (
            int(w * crop_region[0]),
            int(h * crop_region[1]),
            int(w * crop_region[2]),
            int(h * crop_region[3])
        )
        img = img.crop(box)

    # Make square thumbnail
    img = img.resize(size, Image.LANCZOS)

    # Enhance for detail view
    img = ImageEnhance.Sharpness(img).enhance(1.4)
    img = ImageEnhance.Contrast(img).enhance(1.1)

    img.save(output_path, 'JPEG', quality=88, optimize=True)
    print(f"  Thumbnail: {os.path.basename(output_path)} ({size[0]}x{size[1]})")


def create_tinted_variant(input_path, output_path, tint_color, opacity=0.08):
    """Create a subtle color-tinted variant of an image (for visual variety)."""
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Create tint overlay
    overlay = Image.new('RGB', img.size, tint_color)
    img = Image.blend(img, overlay, opacity)

    img = ImageEnhance.Contrast(img).enhance(1.1)
    img.save(output_path, 'JPEG', quality=88, optimize=True)
    print(f"  Variant: {os.path.basename(output_path)}")


def process_all():
    os.chdir(IMG_DIR)

    print("\n=== Processing Main Product Images ===")

    # BULLS-5000 series
    if os.path.exists('product-bulls-5000.jpg'):
        enhance_product_image('product-bulls-5000.jpg', 'product-bulls-5000-hq.jpg')

    # BULLS-3900 (used for 3500)
    if os.path.exists('product-bulls-3900.jpg'):
        enhance_product_image('product-bulls-3900.jpg', 'product-bulls-3900-hq.jpg')

    # PM2000
    if os.path.exists('product-pm2000.png'):
        enhance_product_image('product-pm2000.png', 'product-pm2000-hq.jpg')

    # LS1000
    if os.path.exists('product-ls1000.png'):
        enhance_product_image('product-ls1000.png', 'product-ls1000-hq.jpg')

    # Fixtures
    if os.path.exists('fixture-round.png'):
        enhance_product_image('fixture-round.png', 'fixture-round-hq.jpg')

    # Company reception
    if os.path.exists('company-reception.jpg'):
        img = Image.open('company-reception.jpg')
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Resize to max 900px wide
        if img.width > 900:
            ratio = 900 / img.width
            img = img.resize((900, int(img.height * ratio)), Image.LANCZOS)
        img = ImageEnhance.Contrast(img).enhance(1.1)
        img = ImageEnhance.Brightness(img).enhance(1.05)
        img = ImageEnhance.Color(img).enhance(1.1)
        img.save('company-reception-hq.jpg', 'JPEG', quality=90, optimize=True)
        print(f"  Enhanced: company-reception-hq.jpg")

    print("\n=== Generating Thumbnails for BULLS-5000A ===")
    # Main product image crops for different angles
    if os.path.exists('product-bulls-5000.jpg'):
        # Thumb 1: full product (scaled down)
        create_detail_crop('product-bulls-5000.jpg', 'thumb-5000-full.jpg', size=(200, 200))
        # Thumb 2: control panel area (bottom portion)
        create_detail_crop('product-bulls-5000.jpg', 'thumb-5000-panel.jpg',
                          crop_region=(0.1, 0.55, 0.9, 1.0), size=(200, 200))
        # Thumb 3: polishing plate area (top portion)
        create_detail_crop('product-bulls-5000.jpg', 'thumb-5000-plate.jpg',
                          crop_region=(0.1, 0.0, 0.9, 0.5), size=(200, 200))
    # Thumb 4: fixture detail (from fixture images)
    if os.path.exists('fixture-wheel.png'):
        create_detail_crop('fixture-wheel.png', 'thumb-5000-fixture.jpg', size=(200, 200))

    print("\n=== Generating Thumbnails for BULLS-3500 ===")
    if os.path.exists('product-bulls-3900.jpg'):
        create_detail_crop('product-bulls-3900.jpg', 'thumb-3500-full.jpg', size=(200, 200))
        create_detail_crop('product-bulls-3900.jpg', 'thumb-3500-panel.jpg',
                          crop_region=(0.1, 0.6, 0.9, 1.0), size=(200, 200))
        create_detail_crop('product-bulls-3900.jpg', 'thumb-3500-plate.jpg',
                          crop_region=(0.05, 0.0, 0.95, 0.45), size=(200, 200))
    if os.path.exists('consumables.png'):
        create_detail_crop('consumables.png', 'thumb-3500-accessories.jpg', size=(200, 200))

    print("\n=== Generating Thumbnails for BULLS-PM2000 ===")
    if os.path.exists('product-pm2000.png'):
        create_detail_crop('product-pm2000.png', 'thumb-pm2000-full.jpg', size=(200, 200))
        # Screen area
        create_detail_crop('product-pm2000.png', 'thumb-pm2000-screen.jpg',
                          crop_region=(0.0, 0.0, 1.0, 0.4), size=(200, 200))
        # Stage/optics area
        create_detail_crop('product-pm2000.png', 'thumb-pm2000-optics.jpg',
                          crop_region=(0.3, 0.0, 1.0, 0.5), size=(200, 200))
    if os.path.exists('fiber-endface.png'):
        create_detail_crop('fiber-endface.png', 'thumb-pm2000-endface.jpg', size=(200, 200))

    print("\n=== Generating Thumbnails for BULLS-LS1000 ===")
    if os.path.exists('product-ls1000.png'):
        create_detail_crop('product-ls1000.png', 'thumb-ls1000-full.jpg', size=(200, 200))
        create_detail_crop('product-ls1000.png', 'thumb-ls1000-panel.jpg',
                          crop_region=(0.0, 0.0, 1.0, 0.5), size=(200, 200))
        create_detail_crop('product-ls1000.png', 'thumb-ls1000-side.jpg',
                          crop_region=(0.0, 0.3, 0.6, 1.0), size=(200, 200))
    if os.path.exists('fiber-patchcord.png'):
        create_detail_crop('fiber-patchcord.png', 'thumb-ls1000-fiber.jpg', size=(200, 200))

    print("\n=== Generating Thumbnails for Fixtures ===")
    if os.path.exists('fixture-round.png'):
        create_detail_crop('fixture-round.png', 'thumb-fixture-round.jpg', size=(200, 200))
    if os.path.exists('fixture-large.png'):
        create_detail_crop('fixture-large.png', 'thumb-fixture-large.jpg', size=(200, 200))
    if os.path.exists('fixture-angle.png'):
        create_detail_crop('fixture-angle.png', 'thumb-fixture-angle.jpg', size=(200, 200))
    if os.path.exists('fixture-holder.png'):
        create_detail_crop('fixture-holder.png', 'thumb-fixture-holder.jpg', size=(200, 200))

    print("\n=== Done! ===")


if __name__ == '__main__':
    process_all()
