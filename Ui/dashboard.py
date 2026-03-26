import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_data():
    speeds = []
    try:
        with open("../server/log.csv") as f:
            for line in f:
                parts = line.strip().split(",")
                speeds.append(float(parts[2]))
    except:
        pass
    return speeds

def update_graph():
    speeds = load_data()   # ✅ MUST be first

    if not speeds:
        root.after(3000, update_graph)
        return

    ax.clear()
    ax.plot(speeds, marker='o')

    ax.set_title("Network Speed Analysis")
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Speed (MB/s)")
    ax.grid(True)

    # ✅ Update label dynamically
    if speeds[-1] < 30:
        label.config(text="Status: ⚠️ Congestion")
    else:
        label.config(text="Status: ✅ Good")

    canvas.draw()

    root.after(3000, update_graph)
    
root = tk.Tk()
root.title("Network Analyzer Dashboard")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
label = tk.Label(root, text="Status: Running", font=("Arial", 12))
label.pack()
update_graph()

root.mainloop()