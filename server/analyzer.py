def analyze(speed):
    speed = float(speed)

    if speed < 10:
        return "⚠️ Congestion"
    elif speed < 25:
        return "Moderate"
    else:
        return "Good"