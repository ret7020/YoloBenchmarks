import socket
from time import sleep
from threading import Thread
from config import *
from socket_utils import *
from os import path

ip = "0.0.0.0"
port = 8001


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
            print("flex")
            print(recv)


if __name__ == "__main__":
    print(f"Run on {ip}:{port}")
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        t = Thread(target=process_client, args=(conn, addr))
