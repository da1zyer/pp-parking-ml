from ultralytics import YOLO
from utils.slots_saver import save_slots
from utils.slots_reader import read_slots
from utils.geometry import determine_parking_status
from utils.image import make_image

car_model = YOLO("./models/car_detection.pt")
slot_model = YOLO("./models/slot_detection.pt")

image_with_slots = "4.jpg"
image_with_cars = "5.jpg"

slots_file_path = "./slots/1.txt"

if __name__ == "__main__":
    
    save_slots(slots_file_path)

    slots = read_slots(slots_file_path)

    # Получаем выделения машин

    cars = car_model(image_with_cars, conf=0.5)

    cars_list = []

    for car in cars:
        corners_data = car.obb.xyxyxyxy.cpu().numpy() 
        for points in corners_data:
            cars_list.append(points)

    statuses = determine_parking_status(slots, cars_list)

    # Вывод результатов
    print(f"{'ID места':<10} | {'IoU':<10} | {'Статус'}")
    print("-" * 40)
    for res in statuses:
        print(f"{res['slot_id']:<10} | {res['iou']:<10} | {res['status']}")

    make_image(slots_file_path, image_with_cars, car_model, "result.jpg")
