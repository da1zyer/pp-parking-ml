import json
import os
from pathlib import Path
from PIL import Image
from collections import defaultdict

# ====== Настройки ======
coco_json = r"../data/valid/_annotations.coco.json"        # путь к COCO JSON
images_dir = r"../data/valid"                 # папка с изображениями (train/val)
labels_dir = r"../data/valid_labels"                 # папка, куда сохранять YOLO аннотации

os.makedirs(labels_dir, exist_ok=True)

# ====== Загрузка COCO JSON ======
with open(coco_json) as f:
    data = json.load(f)

# ====== Создаем mapping category_id -> class_id ======
category_map = {cat['id']: idx for idx, cat in enumerate(data['categories'])}

# ====== Группировка аннотаций по image_id ======
annotations_by_image = defaultdict(list)
for ann in data['annotations']:
    annotations_by_image[ann['image_id']].append(ann)

# ====== Конвертация ======
for img_info in data['images']:
    image_id = img_info['id']
    file_name = img_info['file_name']
    w, h = img_info['width'], img_info['height']

    img_path = os.path.join(images_dir, file_name)
    if not os.path.exists(img_path):
        print(f"Image {file_name} not found, skipping")
        continue

    label_file = os.path.join(labels_dir, Path(file_name).stem + ".txt")
    anns = annotations_by_image.get(image_id, [])

    with open(label_file, "w") as f:
        for ann in anns:
            class_id = category_map.get(ann['category_id'], 0)
            x_min, y_min, bbox_w, bbox_h = ann['bbox']

            # Преобразуем в YOLO формат
            x_center = (x_min + bbox_w/2) / w
            y_center = (y_min + bbox_h/2) / h
            bbox_w /= w
            bbox_h /= h

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n")

print("Конвертация COCO -> YOLO завершена!")
