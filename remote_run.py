import os
from struct import pack, unpack
from json import loads, dumps
import base64
import socket

ip = "localhost"
port = 8001


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


def ask_file(conn, file_path, asked_file):
    send_json({"type": "ask_files", "filename": asked_file})
    receive_file(conn, file_path)


def ask(conn, type: str):
    send_json(conn, {"type": type})
    return receive_json(conn)


if __name__ == "__main__":
    print("try to found test.py")
    try:
        from test import run_video_test

        print("file found")
        sock = socket.socket()
        sock.connect((ip, port))
    except ModuleNotFoundError:
        sock = socket.socket()
        sock.connect((ip, port))
        ask_file(sock, "", "test.py")
        print("file downloaded")

        from test import run_video_test
        print("file imported")

    models = ask("models")
