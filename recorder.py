import os 
import wave
import time
import threading
import tkinter as tk
import pyaudio
import pyttsx3
from gtts import gTTS


from speech2text import speech_to_text
from llm import LLM

SPANISH_LANG = {
    "tts": 'es',
    "prompt": 'Spanish'
}

HINDI_LANG = {
    "tts": 'hi-In',
    "prompt": 'English'
}

class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.message = tk.StringVar()
        self.button = tk.Button(self.root, textvariable=self.message, font=("Arial", 120, "bold"), command=self.click_handler)
        self.message.set("Record")
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.llm = LLM(model_name="openai")
        self.language = HINDI_LANG # change this
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

        file_name = "recording.wav"
        
        sound_file = wave.open(file_name, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))

        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

        # finish getting audio, file saved
        # call the transcription tool

        response_text = speech_to_text(file_name)

        self.message.set(response_text)

        # call llm here
        print(self.language)
        result = self.llm.respond(response_text)
        print(result)


        self.message.set(result)

        tts = gTTS(result)
        tts.save("output.mp3")

        # Play the generated speech
        os.system("afplay output.mp3")  # macOS

        return response_text


VoiceRecorder()