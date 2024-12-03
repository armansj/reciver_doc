import socket
import subprocess
import os

def receive_file():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 6000))
    s.listen(1)
    print("Waiting for file from Windows...")

    client_socket, address = s.accept()
    print(f"Connection from {address}")

    file_name_length = client_socket.recv(4)
    if not file_name_length:
        print("Error receiving file name length")
        client_socket.close()
        s.close()
        return
    file_name_length = int.from_bytes(file_name_length, byteorder='big')

    file_name = client_socket.recv(file_name_length).decode()
    print(f"Received file name: {file_name}")

    file_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file_data += data

    print("File received")

    with open(file_name, 'wb') as f:
        f.write(file_data)

    print(f"File saved as {file_name}")

    open_file(file_name)

    client_socket.close()
    s.close()


def open_file(file_path):
    subprocess.run(["open", file_path])


if __name__ == "__main__":
    receive_file()
