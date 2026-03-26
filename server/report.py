import csv

def generate_report():
    min_speed = float('inf')
    busiest_time = ""

    max_speed = 0
    fastest_time = ""

    speeds = []

    with open("log.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            timestamp = row[0]
            speed = float(row[2])

            speeds.append(speed)

            # Find busiest (slowest)
            if speed < min_speed:
                min_speed = speed
                busiest_time = timestamp

            # Find fastest
            if speed > max_speed:
                max_speed = speed
                fastest_time = timestamp

    avg_speed = sum(speeds) / len(speeds)

    print("\n--- NETWORK ANALYSIS REPORT ---")
    print(f"Average Speed: {avg_speed:.2f} MB/s")
    print(f"Fastest Time: {fastest_time} ({max_speed:.2f} MB/s)")
    print(f"Busiest Time (Congestion): {busiest_time} ({min_speed:.2f} MB/s)")