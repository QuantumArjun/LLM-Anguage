import os 
import wave
import time
import threading
import tkinter as tk
import pyaudio

from speech2text import speech_to_text

class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(self.root, text="Record", font=("Arial", 120, "bold"), command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()
    

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start

            seconds = int(passed % 60)
            mins = int(passed / 60 % 60)
            hours = int(passed / 60 / 60 % 60)
            self.label.config(text=f"{hours:02d}:{mins:02d}:{seconds:02d}")
            self.root.update()
    
        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1

        file_name = f"recording{i}.wav"
        while exists:
            if os.path.exists(file_name):
                i += 1  
            else:
                exists = False
        
        sound_file = wave.open(file_name, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))

        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

        # finish getting audio, file saved
        # call the transcription tool

        response_text = speech_to_text(file_name)

        print("hold up")

        self.button.config(text=response_text)


VoiceRecorder()