from logger import log_data
from analyzer import analyze
ui_callback = None

def set_ui_callback(func):
    global ui_callback
    ui_callback = func
FILE_NAME = "testfile.dat"

def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")

    while True:
        try:
            # SEND FILE
            with open(FILE_NAME, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    conn.sendall(data)

            conn.sendall(b"END")

            # RECEIVE SPEED
            result = conn.recv(1024).decode()
            if not result:
                break

            print("CALLING LOGGER...")
            log_data(addr[0], result)

            status = analyze(result)
           
            message = f"{addr[0]} → {result} MB/s | {status}"

            print("[DATA]", message)

            if ui_callback:
                ui_callback(message)

        except:
            break

    conn.close()
    print(f"[-] Disconnected: {addr}")