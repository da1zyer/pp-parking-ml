from ultralytics import YOLO

# Загружаем обученную модель
model = YOLO("runs/detect/parking_model_light2/weights/best.pt")

results = model.predict(
    source=r"../notebooks/datasets/data/images/test/2012-09-12_11_56_00_jpg.rf.041680c3e728940e946ad42134b7362a.jpg",  # путь к изображению
    conf=0.4,                       # порог уверенности (0–1)
    save=True,                      # сохранить результат с боксами
    show=True                       # показать окно с результатом
)
