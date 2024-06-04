from ultralytics.utils.benchmarks import benchmark

benchmark(model="yolov8n.pt", data="coco8.yaml", imgsz=640, device="cpu")