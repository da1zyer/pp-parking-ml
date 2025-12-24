import sys

def delete_slot(slot_id: int, slots_path: str = "../slots/1.txt", buffer_path: str = "../slots/buffer.txt") -> None:
    """
    Удаляет ошибочно определенный парковочный слот из файла
    """
    if not slot_id:
        slot_id = sys.argv[1]

    buffer_file = open(buffer_path, "w")
    file = open(slots_path, "r")
    for line in file:
        buffer_file.write(line)
    file.close()
    buffer_file.close()

    with open(slots_path, "w") as f:
        with open(buffer_path, "r") as b:
            for line in b:
                if (int(line.strip().split()[0]) == slot_id):
                    continue
                f.write(line)

if __name__ == "__main__":
    delete_slot()