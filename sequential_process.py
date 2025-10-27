import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = "data_set"
OUTPUT_DIR = "output_seq"
TARGET_SIZE = (128, 128)
WATERMARK_TEXT = "CortexNoob_X"
WATERMARK_OPACITY = 120
WATERMARK_MARGIN = 6
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def add_watermark(image, text, opacity=120, margin=6):
    base = image.convert("RGBA")
    txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = base.width - text_width - margin
    y = base.height - text_height - margin
    
    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
    return Image.alpha_composite(base, txt_layer).convert("RGB")


def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB").resize(TARGET_SIZE, Image.LANCZOS)
            img = add_watermark(img, WATERMARK_TEXT, opacity=WATERMARK_OPACITY, margin=WATERMARK_MARGIN)
            ext = os.path.splitext(output_path)[1].lower()
            if ext == ".png":
                img.save(output_path, format="PNG", quality=95)
            else:
                img.save(output_path, format="JPEG", quality=90)
    except Exception as e:
        print(f"[ERROR] {input_path}: {e}")

def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"Directory '{INPUT_DIR}' not found.")
        sys.exit(1)

    ensure_dir(OUTPUT_DIR)
    tasks = []
    file_count = 0

    for root, _, files in os.walk(INPUT_DIR):
        rel_dir = os.path.relpath(root, INPUT_DIR)
        rel_dir = "" if rel_dir == "." else rel_dir
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in SUPPORTED_EXTS:
                src = os.path.join(root, fname)
                dst_dir = os.path.join(OUTPUT_DIR, rel_dir)
                ensure_dir(dst_dir)
                dst = os.path.join(dst_dir, os.path.splitext(fname)[0] + ".jpg")
                tasks.append((src, dst))
                file_count += 1

    if file_count == 0:
        print("No images found.")
        sys.exit(1)

    print(f"Found {file_count} images. Processing...")
    t0 = time.perf_counter()

    for src, dst in tasks:
        process_image(src, dst)

    print(f"Sequential Processing Time: {time.perf_counter() - t0:.2f} seconds")

if __name__ == "__main__":
    main()
