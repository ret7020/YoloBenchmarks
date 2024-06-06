import socket
from time import sleep
from threading import Thread
from config import *
from socket_utils import *
from os import path

ip = "0.0.0.0"
port = 8001


def process_client(conn, addr):
    print("Phase 1 started")
    # step 0, send available models
    send_json(conn, models)

    # step 1 and 2, recv chosen models and them
    need_models = receive_json(conn)  # recv in ["model type"]
    for model_name in need_models:
        send_file(path.join(abs_path, model_name))
        print(f"send {model_name}")

    # step 3, send required videos
    need_videos = receive_json(conn)  # recv in ["model type"]
    for video_name in need_videos:
        send_file(path.join(abs_path, video_name))
        print(f"send {video_name}")
    print("Phase 1 finished")


if __name__ == "__main__":
    print(f"Run on {ip}:{port}")
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        t = Thread(target=process_client, args=(conn, addr))
