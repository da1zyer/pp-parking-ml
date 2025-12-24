def read_slots(file_path: str) -> list[dict]:
    """
    Читает точки выделений парковочных мест из файла
    Конвертирует точки из формата 
    "id x1 y1 x2 y2 x3 y3 x4 y4"
    в [{'id': id, 'points': [(x1,y1), ..., (x4,y4)]}, {...}]
    """
    slots = []

    with open(file_path, "r") as f:
        for line in f:
            slot = list(map(float, line.strip().split()))
            slot_id = int(slot[0])
            slot_points = slot[1:]
            
            points = list(zip(slot_points[0::2], slot_points[1::2]))
            
            slots.append({'id': slot_id, 'points': points})
    
    return slots