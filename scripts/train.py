from ultralytics import YOLO

model = YOLO("yolo11s.pt")

# Тренировка
model.train(
    data=r"../parking.yaml",
    epochs=10,          
    imgsz=320,             
    batch=4,           
    name="parking_model_light", 
    workers=2,         
    device="cpu",        
    augment=True,           
    patience=10             
)
