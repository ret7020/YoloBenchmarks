from ultralytics import YOLO

model = YOLO("best.pt")
res = model.predict("./assets/images/bus.jpg", task="detect", verbose=False, optimize=True)
print(res[0].speed["inference"])