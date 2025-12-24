from .image import *
import os

def process_files_sorted(folder_path):
    print(f"--- Проверка папки: {folder_path} ---")

    try:
        all_entries = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Ошибка: Папка не найдена по пути '{folder_path}'")
        return
    except Exception as e:
        print(f"Произошла ошибка при чтении папки: {e}")
        return

    file_paths = []
    for entry in all_entries:
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            file_paths.append(full_path)

    file_paths.sort()

    print(f"Найдено и отсортировано {len(file_paths)} файлов.")
    print("-" * 30)

    return file_paths



def process_timeline(car_model_path, with_slots=True, with_cars=False):
    target_directory = r'C:\code\pp-parking\pp-parking-ml\timeline' 
    images = process_files_sorted(target_directory)
    for i in range(len(images)):
        make_image(f"./slots/{1}.txt", images[i], car_model_path, "result.png", with_slots=with_slots, with_cars=with_cars)