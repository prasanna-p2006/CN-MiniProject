import socket
import ssl
import time

SERVER_IP = "192.168.137.249"
PORT = 5001
FILE_NAME = "C:\\Users\\Public\\downloaded.dat"

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

secure_sock = context.wrap_socket(sock, server_hostname=SERVER_IP)
secure_sock.connect((SERVER_IP, PORT))

start_time = time.time()

with open(FILE_NAME, 'wb') as f:
    while True:
        data = secure_sock.recv(1024)
        if not data:
            break
        f.write(data)

end_time = time.time()

secure_sock.close()

download_time = end_time - start_time
file_size = 10 * 1024 * 1024  # adjust based on file size

speed = file_size / download_time / (1024*1024)

print("Download Time:", download_time)
print("Speed:", speed, "MB/s")

log = open("log.txt", "a")
log.write(f"{time.ctime()} - {speed} MB/s\n")
log.close()