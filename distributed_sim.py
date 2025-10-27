import os
import time
from multiprocessing import Process, Manager
from PIL import Image, ImageDraw

INPUT_DIR = "data_set"
OUTPUT_DIR = "output_distributed"

WATERMARK_TEXT = "Waqas"

IMG_SIZE = (128, 128)

def process_images(image_list, node_id, timings_dict):
    start_time = time.time()
    node_output = os.path.join(OUTPUT_DIR, f"node_{node_id}")
    os.makedirs(node_output, exist_ok=True)

    for img_path in image_list:
        img = Image.open(img_path)
        img = img.resize(IMG_SIZE)
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), WATERMARK_TEXT, fill=(255, 255, 255))

        img_name = os.path.basename(img_path)
        img.save(os.path.join(node_output, img_name))

    end_time = time.time()
    timings_dict[node_id] = round(end_time - start_time, 2)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    all_images = []
    for root, _, files in os.walk(INPUT_DIR):
        for f in files:
            all_images.append(os.path.join(root, f))

    total_images = len(all_images)
    chunk_1 = all_images[: total_images // 2]
    chunk_2 = all_images[total_images // 2 :]

    manager = Manager()
    timings = manager.dict()

    node1 = Process(target=process_images, args=(chunk_1, 1, timings))
    node2 = Process(target=process_images, args=(chunk_2, 2, timings))

    start = time.time()
    node1.start()
    node2.start()
    node1.join()
    node2.join()
    end = time.time()

    total_time = round(end - start, 2)

    SEQ_TIME = 7.85 
    efficiency = round(SEQ_TIME / total_time, 2)

    print("\n===== Distributed Processing Summary =====")
    print(f"Node 1 processed {len(chunk_1)} images in {timings[1]:.2f}s")
    print(f"Node 2 processed {len(chunk_2)} images in {timings[2]:.2f}s")
    print(f"Total distributed time: {total_time:.2f}s")
    print(f"Efficiency: {efficiency:.2f}x over sequential")
    print(f"Sequential Time: {SEQ_TIME:.2f}s")
    print("==========================================\n")

if __name__ == "__main__":
    main()
