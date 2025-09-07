import serial
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque

ser = serial.Serial("COM9", 115200)

plt.ion()
fig, (ax_radar, ax_graph) = plt.subplots(1, 2, figsize=(12, 6))

# --- Radar setup ---
ax_radar = plt.subplot(121, polar=True)
ax_radar.set_ylim(0, 200)           # limit radar to 300 cm
ax_radar.set_thetamin(0)
ax_radar.set_thetamax(180)

# --- Graph setup ---
ax_graph = plt.subplot(122)
ax_graph.set_ylim(0, 200)
ax_graph.set_xlabel("Time (s)")
ax_graph.set_ylabel("Distance (cm)")
ax_graph.set_title("Distance vs Time")

times, distances = [], []
start_time = time.time()

# FIR filter setup (5 taps)
fir_coeffs = [0.1, 0.15, 0.2, 0.25, 0.3]   # weights sum = 1
buffer = deque([0]*len(fir_coeffs), maxlen=len(fir_coeffs))

def fir_filter(new_val):
    buffer.append(new_val)
    return sum(c * x for c, x in zip(fir_coeffs, buffer))

# Spike detection threshold
SPIKE_THRESHOLD = 50 # cm

while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        raw_distance = int(line)
        distance = fir_filter(raw_distance)   # FIR filtered

        # Spike detection
        spike_detected = abs(raw_distance - distance) > SPIKE_THRESHOLD

        # --- Radar ---
        ax_radar.clear()
        ax_radar.set_ylim(0, 200)
        ax_radar.set_thetamin(0)
        ax_radar.set_thetamax(180)

        # draw range rings every 25 cm
        for r in range(0, 201, 25):
            ax_radar.plot(np.linspace(0, np.pi, 200), [r]*200, 'k--', linewidth=0.8)

        theta = np.radians(90)  # fixed forward direction
        ax_radar.plot([theta], [distance], 'bo', label="Filtered")

        if spike_detected:
            ax_radar.plot([theta], [raw_distance], 'ro', label=f"Spike: {raw_distance}cm")
            ax_radar.legend(loc="upper right", fontsize=8)

        ax_radar.set_title("Radar (Max 300 cm)")

        # --- Distance vs Time ---
        t = time.time() - start_time
        times.append(t)
        distances.append(distance)
        ax_graph.clear()
        ax_graph.plot(times, distances, 'b-', label="Filtered")
        ax_graph.set_ylim(0, 300)
        ax_graph.set_xlabel("Time (s)")
        ax_graph.set_ylabel("Distance (cm)")

        if spike_detected:
            ax_graph.plot(t, raw_distance, 'ro')
            # Add annotation box with value
            ax_graph.annotate(f"{raw_distance} cm",
                              xy=(t, raw_distance),
                              xytext=(t, raw_distance+20),
                              arrowprops=dict(facecolor="red", shrink=0.05),
                              bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7))

        ax_graph.legend(loc="upper right", fontsize=8)
        ax_graph.set_title("Distance vs Time")

        plt.pause(0.01)

    except Exception as e:
        print("Error:", e)
        continue
