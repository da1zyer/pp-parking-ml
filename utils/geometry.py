from shapely.geometry import Polygon

def calculate_iou(s_points: list[tuple], c_points: list[tuple]) -> float:
    """
    Вычисляет IoU (Intersection over Union) для двух OBB

    Аргументы передавать в формате [(x1,y1), ..., (x4,y4)]
    """
    # Создаем полигоны
    poly_s = Polygon(s_points)
    poly_c = Polygon(c_points)

    # Проверка геометрии
    if not poly_s.is_valid or not poly_c.is_valid:
        return 0.0

    # Вычисляем пересечение
    intersection = poly_s.intersection(poly_c).area
    
    if intersection == 0:
        return 0.0

    # Вычисляем объединение
    union = poly_s.union(poly_c).area

    iou = intersection / union
    return iou

def determine_parking_status(slots, cars) -> list[dict]:
    """
    Определяет статус каждого парковочного места

    slots передавать в формате [{'id': id, 'points': [(x1,y1), ..., (x4,y4)]}, {...}]
    cars передавать в формате [[(x1,y1), ..., (x4,y4)], [...]]
    """
    results = []

    for slot in slots:
        slot_points = slot['points']
        slot_id = slot['id']
        
        max_iou = 0.0
        
        # Проверяем пересечение данного места со всеми машинами
        for car_points in cars:
            iou = calculate_iou(slot_points, car_points)
            if iou > max_iou:
                max_iou = iou
        
        status = ""
        if max_iou < 0.1:
            status = "free"
        elif 0.1 <= max_iou < 0.5:
            status = "partially_occupied"
        elif max_iou >= 0.5:
            status = "occupied"
            
        results.append({
            "slot_id": slot_id,
            "iou": round(max_iou, 4),
            "status": status
        })
        
    return results