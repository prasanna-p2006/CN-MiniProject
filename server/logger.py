from datetime import datetime

def log_data(client_ip, speed):
    print("LOGGING:", client_ip, speed)
    with open("log.csv", "a") as f:
        f.write(f"{datetime.now()},{client_ip},{speed}\n")