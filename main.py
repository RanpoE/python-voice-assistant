import pyttsx3 as tts
import speech_recognition
import openai
import sys
import threading
import tkinter as tk
import sounddevice  # avoids ASLA warning message.
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("API_KEY", None)


class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.root = tk.Tk()
        self.label = tk.Label(text="E", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def create_file(self):
        return "hello"

    def generate_reponse(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5
        )
        return response["choices"][0]["text"]

    def handle_end(self):
        self.text_to_voice("Exiting the matrix")
        self.root.destroy()
        sys.exit()

    def text_to_voice(self, text):
        self.label.config(fg="blue")
        self.speaker.say(text)
        self.speaker.runAndWait()
        self.speaker.stop()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    if "query" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.handle_end()
                        else:
                            if text is not None:
                                response = self.generate_reponse(text)
                                self.text_to_voice(response)
                            self.label.config(fg="black")
                    if "terminate" in text:
                        self.handle_end()
            except Exception:
                self.label.config(fg="black")
                continue


# Use microphone
Assistant()
