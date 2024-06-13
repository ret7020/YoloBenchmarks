import os
from ultralytics import YOLO
from termcolor import colored
from datetime import datetime
import csv

IMAGES_PATH = "/content/drive/MyDrive/YoloModelsCoco"
DATASET = "coco128.yaml"
CSV_HEADER = ["model", "map50", "map75"]


def csv_init():
    date = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    path = f'./metrics/res_{date}.csv'
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADER)
        writer.writeheader()
    return path


if __name__ == "__main__":
    res_name = csv_init()
    all_models = os.listdir(IMAGES_PATH)
    print(f"Going to test: {len(all_models)} models")
    for model_name in all_models:
        model = YOLO(os.path.join(IMAGES_PATH, model_name))
        metrics = model.val(data=DATASET, verbose=False, save=False, visualize=False)
        res = {"model": model_name, "map50": metrics.box.map50, "map75": metrics.box.map75}
        print(colored(f"Tests result: {res}", "green"))
        with open(res_name, "a") as fd:
            writer = csv.DictWriter(fd, fieldnames=CSV_HEADER)
            writer.writerow(res)
