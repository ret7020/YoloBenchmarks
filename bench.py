# from ultralytics.utils.benchmarks import benchmark

# benchmark(model="yolov8n.pt", data="coco8.yaml", imgsz=640, half=False, device="cpu")

from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.export(format='ncnn', half=True, imgsz=640)
ncnn_model = YOLO("./yolov8n.onnx")

ncnn_speeds = []

for i in range(100):
    ncnn_results = ncnn_model("./assets/images/bus.jpg", verbose=False)
    ncnn_speeds.append(ncnn_results[0].speed["inference"])

print(f'AVG NCNN: {sum(ncnn_speeds) / len(ncnn_speeds)}')

n_speeds = []

for i in range(100):
    n_results = model("./assets/images/bus.jpg", verbose=False)
    n_speeds.append(n_results[0].speed["inference"])

print(f'AVG yoloN: {sum(n_speeds) / len(n_speeds)}')