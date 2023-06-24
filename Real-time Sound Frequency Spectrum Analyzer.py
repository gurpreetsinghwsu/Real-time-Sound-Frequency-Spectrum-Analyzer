import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd

# Settings for audio recording and visualization
duration = 10  # Duration of recording in seconds
fs = 44100  # Sampling frequency
update_interval = 0.1  # Update interval for the plot in seconds

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_title("Real-time Frequency Spectrum")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_xlim(0, fs / 2)
ax.set_ylim(0, 100)
ax.grid(True)

# Initialize variables for real-time plotting
frames_per_buffer = int(fs * update_interval)
frequency = np.linspace(0, fs / 2, frames_per_buffer // 2)
magnitude = np.zeros(frames_per_buffer // 2)

# Callback function for audio streaming
def audio_callback(indata, frames, time, status):
    # Compute the frequency spectrum using Fast Fourier Transform (FFT)
    fft = np.fft.fft(indata[:, 0], frames_per_buffer)
    magnitude[:] = 20 * np.log10(np.abs(fft)[:frames_per_buffer // 2])

def update_plot(frame):
    line.set_data(frequency, magnitude)
    return line,

# Start audio streaming
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs)
stream.start()

# Start the live visualization
ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=update_interval * 1000)

# Show the plot
plt.show()

# Stop audio streaming
stream.stop()
stream.close()
