import speech_recognition as sr

def speech_to_text(file_path):
    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(file_path) as source:
        # Read the audio data from the file
        audio_data = recognizer.record(source)

        try:
            # Convert speech to text
            text = recognizer.recognize_google(audio_data, language='es')
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # Specify the path to the WAV file
# wav_file_path = "recording3.wav"

# # Convert speech to text
# result = speech_to_text(wav_file_path)

# if result:
#     print("Converted Text:")
#     print(result)