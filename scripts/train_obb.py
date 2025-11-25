from ultralytics import YOLO

model = YOLO('yolo11s-obb.pt')

model.train(
    data="../dataset/data.yaml",
    imgsz=512,
    epochs=70,
    batch=8,
    workers=4,
    device=0,
    name="car_obb",
    optimizer="AdamW",
    pretrained=True
)
