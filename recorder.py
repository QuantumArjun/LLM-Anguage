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

'''
Todo
- Chain the continued responses together 
- Better Prompt Engineering for the conversation itself 
- UI Improvements
- Allow people to change the language 
'''

class GUI:
    def __init__(self):
        
        #Initialize tkinter interface
        self.init_interface()

        # Initialized the LLM
        self.llm = LLM(model_name="openai")

        # Initialized the Language
        self.language = HINDI_LANG # change this

        # Begin the main game loop
        self.root.mainloop()
    
    def init_interface(self):
        self.root = tk.Tk()

        # Conversation Frame       
        self.conversation_frame = tk.Frame(self.root, bg="#444654", width=600, height=600)
        # self.conversation_frame.grid(row=0, column=0)
        self.conversation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create the chat text widget
        self.chat_text = tk.Text(self.conversation_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#444654")
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the scrollbar
        self.scrollbar = tk.Scrollbar(self.conversation_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.chat_text.yview)
        self.chat_text.config(yscrollcommand=self.scrollbar.set)

        # Record Frame
        self.record_frame = tk.Frame(self.root, bg="#343541")
        self.record_frame.pack(side=tk.BOTTOM)

        self.record_button = tk.Button(self.record_frame, text="Record", command=self.click_handler, bg="#343541")
        self.record_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.time_label = tk.Label(self.record_frame, text="")
        self.time_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.recording = False

    def add_message(self, message):
        #add to conversation frame
        self.chat_text.config(state=tk.NORMAL)
        if message == None:
            message = "No Message Detected"
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
   

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.record_button.config(text="Processing...")
            self.record_button.config(fg="black")
        else:
            self.recording = True
            self.record_button.config(fg="red")
            self.record_button.config(text="Recording...")
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
            self.time_label.config(text=f"{hours:02d}:{mins:02d}:{seconds:02d}")
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

        self.send_audio_to_LLM(file_name)

    def send_audio_to_LLM(self, file_name):
        # finish getting audio, file saved
        # call the transcription tool
        
        response_text = speech_to_text(file_name)

        self.add_message(response_text)

        # call llm here
        print(self.language)
        result = self.llm.respond(response_text)
        print(result)


        self.add_message(result)

        tts = gTTS(result, lang='hi')
        tts.save("output.mp3")

        # Play the generated speech
        os.system("afplay output.mp3")  # macOS



GUI()