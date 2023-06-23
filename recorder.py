import tkinter as tk
import sounddevice as sd
import soundfile as sf

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.record_button = None
        self.stop_button = None
        self.is_recording = False

        self.init_ui()

    def init_ui(self):
        self.record_button = tk.Button(
            self.master, text="Record", command=self.start_recording
        )
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.master, text="Stop", command=self.stop_recording, state=tk.DISABLED
        )
        self.stop_button.pack(pady=5)

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.stream = sd.InputStream(callback=self.callback)
        self.stream.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.stream.stop()

    def callback(self, indata, frames, time, status):
        if self.is_recording:
            with sf.SoundFile("recording.wav", mode="x", samplerate=44100, channels=2) as file:
                file.write(indata)
            print("Saved recording.wav!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Recorder")
    root.geometry("200x100")

    app = AudioRecorder(root)

    root.mainloop()