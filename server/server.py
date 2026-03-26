import socket
import threading
from handler import handle_client
HOST = "0.0.0.0"
PORT = 5002
FILE_NAME = "testfile.dat"

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SERVER] Running on port {PORT}...")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start_server()