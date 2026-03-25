import socket
import time
import os


SERVER_IP = "localhost"   # CHANGE THIS
PORT = 5002
FILE_NAME = "downloaded.dat"

def receive_file(sock):
    import time
    import os

    start_time = time.time()

    with open(FILE_NAME, 'wb') as f:
        while True:
            data = sock.recv(1024)

            if b"END" in data:
                f.write(data.replace(b"END", b""))
                break

            f.write(data)

    end_time = time.time()

    file_size = os.path.getsize(FILE_NAME)
    time_taken = end_time - start_time

    speed = (file_size / (1024 * 1024)) / time_taken

    return speed

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    print("[CLIENT] Connected to server")

    while True:
        # STEP 1: Receive file + measure speed
        speed = receive_file(client)

        print(f"[CLIENT] Speed: {speed:.2f} MB/s")

        # STEP 2: Send result back
        message = f"{speed:.2f}"
        client.send(message.encode())

        print("[CLIENT] Sent speed to server")

        time.sleep(10)  # for testing (later → 3600)


start_client()