import socket
import threading

HOST = "0.0.0.0"
PORT = 5002
FILE_NAME = "testfile.dat"

def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")

    while True:
        try:
            # STEP 1: Send file
            with open(FILE_NAME, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    conn.sendall(data)
                conn.sendall(b"END")

            print(f"[+] File sent to {addr}")

            # STEP 2: Receive speed from client
            result = conn.recv(1024).decode()

            if not result:
                break

            print(f"[DATA] {addr} -> {result}")

        except Exception as e:
            print(f"[!] Error: {e}")
            break

    conn.close()
    print(f"[-] Disconnected: {addr}")


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