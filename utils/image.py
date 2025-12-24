from .slots_reader import read_slots
from .geometry import calculate_iou

COLOR_FREE = (0, 255, 0)       # Зеленый
COLOR_PARTIAL = (0, 255, 255)  # Желтый
COLOR_OCCUPIED = (0, 0, 255)   # Красный
TEXT_COLOR = (255, 255, 255)   # Белый для текста

def draw_transparent_polygon(img, pts, color, alpha=0.4):
    """Рисует полупрозрачную заливку"""
    import cv2
    overlay = img.copy()
    cv2.fillPoly(overlay, [pts], color)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def make_image(slots_path: str, image_path: str, model_path: str, output_path: str, with_slots: bool = True, with_cars: bool = False):
    """
    Генерирует и сохраняет изображение с выделенными парковочными местами
    """
    import cv2
    import numpy as np
    from ultralytics import YOLO # Можно будет обновить на lazy import

    img = cv2.imread(image_path)
    img = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_LINEAR)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть картинку {image_path}")
    
    parking_slots = read_slots(slots_path)

    model = YOLO(model_path)

    results = model(img, conf=0.5, verbose=False)

    cars_list = []

    for r in results:
        if r.obb is not None:
            # Получаем координаты всех машин сразу в numpy (N, 4, 2)
            # N - кол-во машин, 4 - угла, 2 - x и y
            c_points = r.obb.xyxyxyxy.cpu().numpy()
            
            for car in c_points:
                formatted_car = [tuple(pt) for pt in car]
                cars_list.append(formatted_car)
    
    if with_slots:

        for spot in parking_slots:
            max_iou = 0.0
            
            # Находим максимальное пересечение с любой из машин
            for car in cars_list:
                iou = calculate_iou(spot['points'], car)
                if iou > max_iou:
                    max_iou = iou
            
            # Статус и цвет
            if max_iou < 0.1:
                status = "Free"
                color = COLOR_FREE
            elif max_iou < 0.3:
                status = "Partial"
                color = COLOR_PARTIAL
            else:
                status = "Occupied"
                color = COLOR_OCCUPIED

            pts = np.array(spot['points'], np.int32)
            pts = pts.reshape((-1, 1, 2)) # Формат (N, 1, 2) нужен для polylines

            draw_transparent_polygon(img, pts, color, alpha=0.3)
            
            cv2.polylines(img, [pts], isClosed=True, color=color, thickness=1)

            text_pos = tuple(pts[0][0]) 
            label = f"ID:{spot['id']}"
            
            cv2.putText(img, label, (text_pos[0], text_pos[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 1)

    if with_cars:
        for car in cars_list:
            pts = np.array(car, np.int32)
            pts = pts.reshape((-1, 1, 2))

            draw_transparent_polygon(img, pts, TEXT_COLOR, alpha=0.1)
            
            cv2.polylines(img, [pts], isClosed=True, color=TEXT_COLOR, thickness=1)

    cv2.imwrite(output_path, img)