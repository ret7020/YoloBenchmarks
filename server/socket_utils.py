import socket
from json import dumps, loads
from struct import pack, unpack
import base64
from time import sleep


def send_file(sock, file_name):
    # Берём имя файла и проверяем существование файла
    try:
        with open(file_name, "rb") as file:
            file.read()
    except FileNotFoundError:
        print('\x1B[1m' + "Файл не найден" + '\x1B[0m')
        file_name = ""

    print("Начинаем чтение файла")
    # Читаем файл и записываем данные into json
    with open(file_name, "rb") as file:
        file_content = file.read()
    print("Начинаем кодирование файла")
    file_data = {"name": file_name, "content": base64.b64encode(file_content).decode('ascii')}

    # превращаем длину json c файлом в 4 байта
    byte_n = pack('<I', len(dumps(file_data)))
    sock.send(byte_n)

    # Отправляем файл
    sleep(0.1)
    sock.send(dumps(file_data).encode("utf-8"))

    # Проверка, дошло ли наше письмо
    ans = b""
    while len(ans) != 5:
        ans += sock.recv(5)
    if ans.decode("utf-8") == "DO IT":
        print("В теории файл записался")
    else:
        print("Oh Щ.И.Т., we have some problama")


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
        data += connection.recv(size-data)

    return data


def send_string(connection, string):
    send_data(connection, string.encode('utf-8'))


def receive_string(connection):
    return receive_data(connection).decode('utf-8')


def send_json(conn, json):
    send_string(conn, dumps(json))


def receive_json(conn):
    return loads(receive_string(conn))
