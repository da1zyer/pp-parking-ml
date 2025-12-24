import utils.slots_saver
import utils.slots_remover
import utils.image
from utils.timeline import process_timeline
import sys
from pathlib import Path

car_model_path = "./models/car_detection.pt"
slot_model_path = "./models/slot_detection.pt"

if len(sys.argv) < 2:
    option = ""
else:
    option = sys.argv[1]

if option == "save":
    # Путь к картинке и имя файла в параметрах
    slots_count = utils.slots_saver.save_slots(slot_model_path, sys.argv[2], f"./slots/{sys.argv[3]}.txt")
    print("-"*20)
    print(f"Сохранено в /slots/{sys.argv[3]}.txt")
    print(f"Количество мест: {slots_count}")
    print("-"*20)
    
elif option == "delete":
    # Имя файла со слотами и id места в параметрах
    utils.slots_remover.delete_slot(int(sys.argv[3]), f"./slots/{sys.argv[2]}.txt", "./slots/buffer.txt")
    print("-"*20)
    print(f"Слот с id: {sys.argv[3]} удален")
    print("-"*20)

elif option == "process":
    # Имя файла со слотами и путь к изображению
    with_slots = True
    with_cars = False
    if len(sys.argv) == 5:
        if sys.argv[4] == "--cars-only":
            with_slots = False
            with_cars = True
        elif sys.argv[4] == "--with-cars":
            with_slots = True
            with_cars = True
        
    utils.image.make_image(f"./slots/{sys.argv[2]}.txt", sys.argv[3], car_model_path, "result.png", with_slots=with_slots, with_cars=with_cars)
    print("-"*20)
    print("Сохранено в result.png")
    print("-"*20)

elif option == "clear":
    folder = Path("./slots")

    for file in folder.iterdir():
        if file.is_file():
            file.unlink()

    print("-"*20)
    print("Все файлы удалены")
    print("-"*20)

elif option == "timeline":
    process_timeline(car_model_path)

    print("-"*20)
    print("Все файлы удалены")
    print("-"*20)

else:
    print("-"*20)
    print("Команды:\n")
    print("save image_path file_name - создает файл парковки\n")
    print("delete slots_file_name slot_id - удаляет парковочное место из файла\n")
    print("process slots_file_name image_path - создает изображение с классифицированными местами")
    print("--cars-only - выделяет только машины")
    print("--with-cars - выделяет места и машины\n")
    print("clear - удаляет все файлы парковок")
    print("-"*20)