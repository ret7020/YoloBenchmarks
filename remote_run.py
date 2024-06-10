from os import path, makedirs
from struct import pack, unpack
from json import loads, dumps
import base64
import socket



ip = "localhost"
port = 8001
main_dir = "data"
models_path = path.join(main_dir, "models")
videos_path = path.join(main_dir, "videos")

# print(models_path, videos_path)

makedirs(models_path, exist_ok=True)
makedirs(videos_path, exist_ok=True)

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
        data += connection.recv(size - len(data))

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
    with open(path.join(file_path, name), "wb") as file:
        file.write(content)

    conn.send("DO IT".encode("utf-8"))


def ask_file(conn, file_path, asked_file, ftype):
    send_json(conn, {"type": "ask_files", "filename": asked_file, "ftype": ftype})
    receive_file(conn, file_path)


def ask(conn, type: str):
    send_json(conn, {"type": type})
    return receive_json(conn)


if __name__ == "__main__":
    system_name = input("Назовитесь>")
    print("Try to found test.py")
    try:
        from test import bench_model, parse_model_name
        print("File load")

        sock = socket.socket()
        sock.connect((ip, port))
    except ModuleNotFoundError:
        print("File not found")
        sock = socket.socket()
        sock.connect((ip, port))
        ask_file(sock, "", "test.py")
        print("File downloaded")

        from test import bench_model, parse_model_name

        print("File imported")

    from ultralytics import YOLO

    models = ask(sock, "get_models")
    print("Got models")
    want_models = []
    to_test_models = []
    for model_type in models.keys():
        model_use = input(f"Do you want to test {model_type} models? (y - yes, other - not): ")
        if model_use.lower() == "y":
            for model_name in models[model_type]:
                to_test_models.append(model_name)
                if not path.isfile(path.join(models_path, model_name)):
                    want_models.append(model_name)

    if len(want_models) != 0: print(f"We need to download models: {', '.join(want_models)}")
    for model_name in want_models:
        ask_file(sock, models_path, model_name, "model")
        print(f"We downloaded {model_name}")
    
    

    videos = ask(sock, "get_videos")
    if len(videos) != 0: print(f"We need to download videos: {', '.join(videos)} ({len(videos)})")
    for video in videos:
        if not path.isfile(path.join(videos_path, video)):
            ask_file(sock, videos_path, video, "video")
            print(f"Downloaded {video}")

    print("All models and videos downloaded.")

    for video in videos:
        for model_name in to_test_models:
            model = YOLO(path.join(models_path, model_name))
            if not model_name.endswith(".pt"):
                args = parse_model_name(model_name)
            else: args = ()
            res = bench_model(model, path.join(videos_path, video), args)
            print(res)
            send_json(sock, {"type": "send_stats", "save_name": f"{system_name}.csv", "results": {model.ckpt_path: res}})
        

    # TODO: make bench

    # results = {"jisdhfishdf": 2342}
    # 

    sock.close()
