import socket
from time import sleep
from threading import Thread
from config import *
from socket_utils import *
from os import path, makedirs
import csv

ip = "localhost"
port = 8001

makedirs(python_files_path, exist_ok=True)
makedirs(video_path, exist_ok=True)
makedirs(model_path, exist_ok=True)
makedirs(analytics_path, exist_ok=True)


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


def process_client(conn, addr):
    print("Connect from", addr)
    while True:
        recv = receive_json(conn)
        if recv["type"] == "ask_files":
            print(addr, f"asked file {recv["filename"]} from group {recv["ftype"]}")
            file_name = recv["filename"]
            if recv["ftype"] == "py":
                send_file(conn, path.join(python_files_path, file_name))
            elif recv["ftype"] == "video":
                send_file(conn, path.join(video_path, file_name))
            elif recv["ftype"] == "model":
                send_file(conn, path.join(model_path, file_name))
        elif recv["type"] == "get_models":
            print(addr, "asked models")
            send_json(conn, models)
        elif recv["type"] == "get_videos":
            print(addr, "asked videos")
            send_json(conn, videos)
        elif recv["type"] == "send_stats":
            print("Flex, we resive results from", addr)
            csv_benchmark(path.join(analytics_path, recv["save_name"]), recv["results"])


if __name__ == "__main__":
    print(f"Run on {ip}:{port}")
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        t = Thread(target=process_client, args=(conn, addr))
        t.start()
