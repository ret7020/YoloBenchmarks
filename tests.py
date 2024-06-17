from ultralytics import YOLO
import cv2
import gc
import torch

times = []
MANY_CARS = ["./assets/images/cars_many.jpg", 
             "./assets/images/cars_many_1.jpg",
             "./assets/images/cars_many_2.jpg",
             "./assets/images/cars_many_3.jpg"]

SINGLE_CAR = ["./assets/images/single_car.jpg",
              "./assets/images/single_car_1.jpg",
              "./assets/images/single_car_2.jpg",
              "./assets/images/single_car_3.jpg"]

MODELS = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt"]
PER_IMG_INF_CNT = 5

for model in MODELS:
    print("-" * 5 + model + "-" * 5)
    torch.cuda.empty_cache()
    gc.collect()
    m = YOLO(model)
    

    print("Warmup...")
    for _ in range(15): m("./assets/images/bus.jpg", save=False, verbose=False, visualize=False)


    print("Test...")
    for img in MANY_CARS:
        times += [m(cv2.resize(cv2.imread(img), (640, 640)))[0].speed['inference'] for _ in range(PER_IMG_INF_CNT)]

    print(1000 / (sum(times) / len(times)), 1000 / max(times), 1000 / min(times))

    times = []
    torch.cuda.empty_cache()
    del m
    gc.collect()
    m = YOLO(model)
    
    print("Warmup...")
    for _ in range(15): m("./assets/images/bus.jpg", save=False, verbose=False, visualize=False)

    print("Test single cars...")
    for img in SINGLE_CAR:
        times += [m(cv2.resize(cv2.imread(img), (640, 640)))[0].speed['inference'] for _ in range(PER_IMG_INF_CNT)]

    print(1000 / (sum(times) / len(times)), 1000 / max(times), 1000 / min(times))
    del m