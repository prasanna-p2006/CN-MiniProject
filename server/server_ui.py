import socket
import threading
import tkinter as tk
from handler import handle_client, set_ui_callback
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HOST = "localhost"
PORT = 5002

speeds = []  # store speeds

# ---------------- SERVER LOGIC ---------------- #

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    update_log("[SERVER] Running...\n")

    while True:
        conn, addr = server.accept()
        update_log(f"[+] Connected: {addr}")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# ---------------- UI UPDATE FUNCTION ---------------- #

def update_log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

    # extract speed from message
    try:
        parts = message.split("→")[1]
        speed = float(parts.split("MB")[0])
        speeds.append(speed)
    except:
        pass

# ---------------- GRAPH + STATS UPDATE ---------------- #

def update_graph():
    ax.clear()

    if speeds:
        ax.plot(speeds, marker='o')
        ax.set_title("Live Network Speed")
        ax.set_xlabel("Time")
        ax.set_ylabel("Speed (MB/s)")
        ax.grid(True)

        # 🔥 STATS CALCULATION
        avg = sum(speeds) / len(speeds)
        max_s = max(speeds)
        min_s = min(speeds)

        stats_label.config(
            text=f"Avg: {avg:.2f} MB/s | Max: {max_s:.2f} | Min: {min_s:.2f}"
        )

        # 🔥 STATUS
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
root.title("Server Dashboard")

# STATUS LABEL
status_label = tk.Label(root, text="Status: Running", font=("Arial", 12))
status_label.pack()

# STATS LABEL
stats_label = tk.Label(root, text="Avg: 0 | Max: 0 | Min: 0", font=("Arial", 12))
stats_label.pack()

# GRAPH
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# LOG BOX
log_box = tk.Text(root, height=10, width=80)
log_box.pack()

# connect handler → UI
set_ui_callback(update_log)

# start server thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# start graph updating
update_graph()

root.mainloop()