def save_slots(model_path: str, 
               image_path: str, 
               file_path: str, 
               conf: float = 0.5) -> int:
    """
    Сохраняет точки выделений парковочных мест в файл
    в формате "id x1 y1 x2 y2 x3 y3 x4 y4"
    """
    import cv2
    from ultralytics import YOLO # Можно будет обновить на lazy import

    model = YOLO(model_path)

    img = cv2.imread(image_path)
    img = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_LINEAR)

    result = model(img, conf=conf, verbose=False)

    with open(file_path, "w") as slots:
        id = 1
        for r in result:
        # Проверяем, что есть детекции
            if r.obb is None:
                continue

            corners_data = r.obb.xyxyxyxy.cpu().numpy() 
            for points in corners_data:
                # points: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                flat_points = points.flatten() # Приводим к [x1, y1, x2, y2, x3, y3, x4, y4]
                
                points_str = " ".join(map(str, flat_points))
                toWrite = f"{id} {points_str}\n"
                
                slots.write(toWrite)
                id += 1

    return id - 1