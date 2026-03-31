import socket
import threading
import tkinter as tk
import ssl
from handler import handle_client, set_ui_callback
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HOST = "0.0.0.0"   # 🔥 IMPORTANT for network access
PORT = 5002

speeds = []

# ---------------- SSL SETUP ---------------- #

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# ---------------- SERVER LOGIC ---------------- #

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    update_log("[SERVER] Running with SSL...\n")

    while True:
        client_socket, addr = server.accept()

        # 🔐 Wrap with SSL
        conn = context.wrap_socket(client_socket, server_side=True)

        update_log(f"[+] Secure Connected: {addr}")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# ---------------- UI UPDATE FUNCTION ---------------- #

def update_log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

    # extract speed
    try:
        parts = message.split("→")[1]
        speed = float(parts.split("MB")[0])
        speeds.append(speed)
    except:
        pass

# ---------------- GRAPH + STATS ---------------- #

def update_graph():
    ax.clear()

    if speeds:
        ax.plot(speeds, marker='o')
        ax.set_title("Live Network Speed (SSL)")
        ax.set_xlabel("Time")
        ax.set_ylabel("Speed (MB/s)")
        ax.grid(True)

        avg = sum(speeds) / len(speeds)
        max_s = max(speeds)
        min_s = min(speeds)

        stats_label.config(
            text=f"Avg: {avg:.2f} MB/s | Max: {max_s:.2f} | Min: {min_s:.2f}"
        )

        if speeds[-1] < 30:
            status_label.config(text="⚠️ Congestion", fg="red")
            root.configure(bg="#ffe6e6")
        else:
            status_label.config(text="✅ Good", fg="green")
            root.configure(bg="white")

    canvas.draw()
    root.after(2000, update_graph)

# ---------------- MAIN UI ---------------- #

root = tk.Tk()
root.title("Secure Server Dashboard (SSL)")

status_label = tk.Label(root, text="Status: Running", font=("Arial", 12))
status_label.pack()

stats_label = tk.Label(root, text="Avg: 0 | Max: 0 | Min: 0", font=("Arial", 12))
stats_label.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

log_box = tk.Text(root, height=10, width=80)
log_box.pack()

set_ui_callback(update_log)

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

update_graph()

root.mainloop()