import socket
import ssl
import threading

HOST = '0.0.0.0'
PORT = 5001
FILE_NAME = "testfile.dat"

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

def handle_client(conn):
    print("Client connected")

    with open(FILE_NAME, 'rb') as f:
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)

    conn.close()
    print("File sent")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    with context.wrap_socket(server_socket, server_side=True) as ssock:
        print("Server running on port", PORT)

        while True:
            client_conn, addr = ssock.accept()
            thread = threading.Thread(target=handle_client, args=(client_conn,))
            thread.start()

start_server()