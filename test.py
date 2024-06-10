try:
    from ultralytics import YOLO
except ModuleNotFoundError:
    import os
    os.system("pip3 install ultralytics")
import os
from config import *
from tqdm import tqdm
from termcolor import colored
import csv
from datetime import datetime
import psutil
import platform
import cv2
import gc
import torch



TEST_SOURCE_ARGS, CAPTURE = None, None

def bench_model(model, video, args):
    inference_times = []
    is_half = True if "half" in args else False
    is_int8 = True if "int8" in args else False
    optimize = False if "ncnn" in args else True  # NCNN models can't work with optimize flag
    runtime = args[1] if len(args) > 1 else "BASE"

    capture = cv2.VideoCapture(video)

    # Warmup model before benched inference (anyway on test images set, not camera)
    warmup_times = []
    print(colored(f"Testing model: {model.ckpt_path} with video: {video}", "green"))
    for _ in range(10):
        _, frame = capture.read()
        res = model.predict(frame, task=TASK, verbose=False, half=is_half, int8=is_int8, optimize=optimize, save=False, visualize=False)
        warmup_times.append(res[0].speed["inference"])
    print(colored(f"Warmup finished", "green"))

    frames_cnt = 0
    progress_bar = iter(tqdm(range(200)))
    while capture.isOpened():
        ret, frame = capture.read()
        if ret and frames_cnt < 200:
            frame = cv2.resize(frame, (640, 640))
            res = model.predict(frame, task=TASK, verbose=False, half=is_half, int8=is_int8, optimize=optimize, save=False, visualize=False)
            inference_times.append(res[0].speed["inference"])
            frames_cnt += 1
            next(progress_bar)
        else:
            capture.release()
    print(colored(f"Benchmark finished", "yellow"))


    metrics = model.val(data=VALIDATE_CONFIG, verbose=False)
    print(colored(f"Model validated on {VALIDATE_CONFIG}", "yellow"))
    return {
        "inference_time": sum(inference_times) / (len(inference_times)),  # ms
        "inference_time_1": round(sum(inference_times) / (len(inference_times)), 1),  # ms 1 digit
        "inference_time_min": min(inference_times),
        "inference_time_max": max(inference_times),
        "fps": round(1000 / (sum(inference_times) / (len(inference_times))), 1),  # fps 1 digit
        "half": int(is_half),
        "int8": int(is_int8),
        "runtime": runtime,
        "map50": metrics.box.map50,
        "map75": metrics.box.map75,
        "device": "cpu",  # TODO selectable device
        "warmup_min_inf_time": min(warmup_times),
        "warmup_max_inf_time": max(warmup_times)
    }


def benchmark(models, images, repeat_coeff=5, save_callback=lambda x: None):
    print(
        f"Testing models: {len(models)}\nUniq images: {colored(len(images), 'green')}\nInferences count: {colored(str(len(models) * repeat_coeff * len(images)), 'yellow')}")
    results = {}
    for model in tqdm(models):
        args = model[1:] if len(model) > 1 else []
        model = YOLO(model[0])
        results[model.ckpt_path] = bench_model(model, args, images, repeat_coeff=2)
        save_callback(results[model.ckpt_path])

        # Clean system after inference
        del model
        torch.cuda.empty_cache()
        gc.collect()

    return results


def print_benchmark(results):
    for model in results:
        res = results[model]
        rnd_time = f"{res['inference_time_1']} ms"
        rnd_fps = f"{res['fps']} fps"
        inference_time = f"({res['inference_time']} ms)"
        print(f"{colored(model, 'yellow')}: {rnd_time.rjust(10)} {rnd_fps.rjust(10)} {inference_time.rjust(30)}")


def csv_init():
    date = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    path = f'./results/results_{date}.csv'
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADER)
        writer.writeheader()
    return path


def csv_benchmark(path, results):
    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADER)
        for model in results:
            res = results[model]
            # TOOD JOIN
            writer.writerow({'model': model.replace("./exported_models/", "")} | res)


def parse_model_name(name, path):
    name_full = name
    dot_index = name.rfind(".")
    if dot_index != -1: name = name[:dot_index]
    if "_ncnn_model" in name: name = name.replace("_ncnn_model", "")
    if "_openvino_model" in name: name = name.replace("_openvino_model", "")
    base_model, runtime, dtype = name.split("_")
    return f"{path}/{name_full}", base_model, runtime, dtype


def print_machine_info():
    info = {}
    info['platform'] = platform.system()
    info['release'] = platform.release()
    info['version'] = platform.version()
    info['architecture'] = platform.machine()
    info['cpu_cores'] = psutil.cpu_count(logical=False)
    info['cpu_all'] = psutil.cpu_count()
    info['ram'] = f"{psutil.virtual_memory().total / (1024.0 ** 3)} GB"
    print("Current machine data: ")
    for i in info:
        print(f'{colored(i, "green").ljust(30)}: {str(info[i]).ljust(20)}')


def run_video_test(TEST_SOURCE_):
    global TEST_SOURCE_ARGS, CAPTURE
    print_machine_info()
    if not os.path.exists("./results"):
        os.mkdir("./results")
    path = csv_init()
    print(f"Writing csv results to: {colored(path, 'green')}")
    TEST_SOURCE_ARGS = TEST_SOURCE_.split(":")
    if TEST_SOURCE_ARGS[0] == "camera":
        if TEST_SOURCE_ARGS[1].isdigit():
            src = int(TEST_SOURCE_ARGS[1])
        else:
            src = TEST_SOURCE_ARGS[1]
        CAPTURE = cv2.VideoCapture(src)

    print(f"Loaded Base Models ({len(BASE_MODELS)}): {colored(BASE_MODELS, 'green')}")
    if TEST_BASE:  # Test base yolo models
        print(f"Testing BASE models on {colored('cpu', 'yellow')}")
        base_models_results = benchmark(BASE_MODELS, TEST_IMAGES)
        print_benchmark(base_models_results)
        csv_benchmark(path, base_models_results)

    if TEST_EXPORTED:
        exported_models = os.listdir(EXPORTED_MODELS_PATH)
        if MODEL_FILTER:
            exported_models = list(filter(MODEL_FILTER, exported_models))
        print(exported_models)
        print(f"Ready to check exported models: {len(exported_models)}")
        models = [parse_model_name(exported_model, EXPORTED_MODELS_PATH) for exported_model in exported_models]
        print(models)
        results = benchmark(models, TEST_IMAGES)
        csv_benchmark(path, results)


if __name__ == "__main__":
    run_video_test(TEST_SOURCE)
