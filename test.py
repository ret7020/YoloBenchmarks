from ultralytics import YOLO
import os
from config import *
from tqdm import tqdm
from termcolor import colored
import csv
from datetime import datetime
import psutil
import platform
import time
import cv2
import gc
import torch
import sys
import socket
import os
from struct import pack, unpack
from json import loads, dumps
import base64


def send_data(connection, data):
    size = len(data)
    size_bytes = pack("<I", size)
    connection.send(size_bytes)
    connection.send(data)


def receive_data(connection):
    size_bytes = connection.recv(4)
    size = unpack("<I", size_bytes)[0]

    data = b''
    while len(data) < size:
        data += connection.recv(1024)

    return data


def send_string(connection, string):
    send_data(connection, string.encode('utf-8'))


def receive_string(connection):
    return receive_data(connection).decode('utf-8')


def send_json(conn, json):
    send_string(conn, dumps(json))


def receive_json(conn):
    return loads(receive_string(conn))


def receive_file(conn, file_path):
    # Получаем длину json с файлом
    f_len_byte = b""
    while len(f_len_byte) != 4:
        f_len_byte += conn.recv(4)
    json_len = unpack('<I', f_len_byte)[0]

    # Получаем сам json
    json_b = b""
    while len(json_b) != json_len:
        json_b += conn.recv(json_len - len(json_b))
    data_name = loads(json_b.decode("utf-8"))

    # Разбираем json
    name = data_name["name"]
    content = base64.b64decode(data_name["content"])

    # Записываем файл
    with open(file_path + name, "wb") as file:
        file.write(content)

    conn.send("DO IT".encode("utf-8"))


def bench_model(model, args, images, repeat_coeff=5):
    inference_times = []
    is_half = True if "half" in args else False
    is_int8 = True if "int8" in args else False
    optimize = False if "ncnn" in args else True  # NCNN models can't work with optimize flag
    runtime = args[1] if len(args) > 1 else "BASE"

    # Warmup model before benched inference (anyway on test images set, not camera)
    warmup_times = []
    for _ in range(WARMUP_IMAGES):
        res = model.predict(images[0], task=TASK, verbose=False, half=is_half, int8=is_int8, optimize=optimize)
        warmup_times.append(res[0].speed["inference"])

    if TEST_SOURCE_ARGS[0] == "images":
        for _ in range(repeat_coeff):  # test each image repeat_coeff times on same model
            for image in images:
                res = model.predict(image, task=TASK, verbose=False, half=is_half, int8=is_int8, optimize=optimize)
                inference_times.append(res[0].speed["inference"])
                time.sleep(DELAY_BETWEEN_TESTS)
    elif TEST_SOURCE_ARGS[1] == "camera":
        for _ in range(int(TEST_SOURCE_ARGS[2])):
            _, image = CAPTURE.read()
            res = model.predict(image, task=TASK, verbose=False, half=is_half, int8=is_int8, optimize=optimize)
            inference_times.append(res[0].speed["inference"])
            time.sleep(DELAY_BETWEEN_TESTS)

    metrics = model.val(data=VALIDATE_CONFIG, verbose=False)
    return {
        "inference_time": sum(inference_times) / (len(inference_times)),  # ms
        "inference_time_1": round(sum(inference_times) / (len(inference_times)), 1),  # ms 1 digit
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


def benchmark(models, images, repeat_coeff=5):
    print(
        f"Testing models: {len(models)}\nUniq images: {colored(len(images), 'green')}\nInferences count: {colored(str(len(models) * repeat_coeff * len(images)), 'yellow')}")
    results = {}
    for model in tqdm(models):
        args = model[1:] if len(model) > 1 else []
        model = YOLO(model[0])
        results[model.ckpt_path] = bench_model(model, args, images, repeat_coeff=2)

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
            writer.writerow({'model': model, 'inference_time': res['inference_time_1'],
                             'fps': res['fps'], 'accurate_time': res['inference_time'],
                             'half': res["half"], 'int8': res["int8"], 'runtime': res["runtime"], 'mAP50': res['map50'],
                             'mAP75': res['map75'], 'device': res['device']})


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
