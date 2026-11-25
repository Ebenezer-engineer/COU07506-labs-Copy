
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Signal settings
fs = 100
heart_rate = 72
window = 6

# Continuous sample counter
sample_count = 0

# Store incoming samples
buffer_size = fs * window
y_buffer = np.zeros(buffer_size)

fig, ax = plt.subplots(figsize=(12, 4))

line, = ax.plot([], [], color="red", linewidth=2)

ax.set_xlim(0, window)
ax.set_ylim(-0.2, 1.2)

ax.set_title("REAL-TIME PPG MONITOR")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("PPG Amplitude")
ax.grid(True)

# Generate one PPG sample at a time
def generate_ppg(t):
    period = 60 / heart_rate
    phase = (t % period) / period

    systolic = np.exp(-0.5 * ((phase - 0.20)/0.065)**2)
    notch = -0.10 * np.exp(-0.5 * ((phase - 0.40)/0.025)**2)
    diastolic = 0.30 * np.exp(-0.5 * ((phase - 0.55)/0.10)**2)

    return systolic + notch + diastolic

def update(frame):
    global sample_count, y_buffer

    # Generate new samples
    new_samples = 5

    for _ in range(new_samples):
        current_time = sample_count / fs

        value = generate_ppg(current_time)

        # Shift old samples to the left
        y_buffer[:-1] = y_buffer[1:]

        # Add newest sample on the right
        y_buffer[-1] = value

        sample_count += 1

    # Plot complete moving window
    x = np.arange(buffer_size) / fs

    line.set_data(x, y_buffer)

    return line,

ani = FuncAnimation(
    fig,
    update,
    interval=50,
    blit=False,
    cache_frame_data=False
)

plt.show()
