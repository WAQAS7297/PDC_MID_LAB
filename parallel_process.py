import os
import time
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = "data_set"
OUTPUT_BASE = "output_parallel"
TARGET_SIZE = (128, 128)
WATERMARK_TEXT = "CortexNoob_X"
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
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = base.width - tw - margin
    y = base.height - th - margin

    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
    return Image.alpha_composite(base, txt_layer).convert("RGB")


def process_one(args):
    src, dst = args
    try:
        with Image.open(src) as img:
            img = img.convert("RGB")
            img = img.resize(TARGET_SIZE, Image.LANCZOS)
            img = add_watermark(img, WATERMARK_TEXT)
            img.save(dst, "JPEG", quality=90)
    except Exception as e:
        print(f"Error: {src} -> {e}")


def build_tasks(output_dir):
    tasks = []
    for root, _, files in os.walk(INPUT_DIR):
        rel = os.path.relpath(root, INPUT_DIR)
        rel = "" if rel == "." else rel

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SUPPORTED_EXTS:
                src = os.path.join(root, f)
                dst_folder = os.path.join(output_dir, rel)
                ensure_dir(dst_folder)
                dst = os.path.join(dst_folder, os.path.splitext(f)[0] + ".jpg")
                tasks.append((src, dst))
    return tasks


def run_parallel(workers):
    output_dir = os.path.join(OUTPUT_BASE, f"{workers}_workers")
    ensure_dir(output_dir)
    tasks = build_tasks(output_dir)

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as exe:
        exe.map(process_one, tasks)
    return time.perf_counter() - start


def main():
    cpu_count = os.cpu_count()
    print("\n Starting Parallel Processing Test")
    print("===================================")
    print(f"Detected CPU Cores: {cpu_count}\n")

    worker_configs = [1, 2, 4, 8, cpu_count]
    worker_configs = sorted(set(min(w, cpu_count) for w in worker_configs))

    results = {}

    for w in worker_configs:
        print(f"\nProcessing with {w} workers...")
        t = run_parallel(w)
        results[w] = round(t, 2)
        print(f" Workers: {w} | Time: {t:.2f}s")

    base_time = results[1]

    print("\n\n Parallel Speedup Table")
    print("Workers | Time (s) | Speedup")
    print("------- | -------- | -------")
    for w, t in results.items():
        speedup = round(base_time / t, 2)
        print(f"{w:<7} | {t:<8.2f} | {speedup:.2f}x")

    print("\nSequential Time (Baseline): {:.2f}s".format(base_time))



if __name__ == "__main__":
    main()
