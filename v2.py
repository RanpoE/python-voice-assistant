import openai
import speech_recognition as sr
import pyttsx3
import time
import sounddevice


openai.api_key = "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"
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source=source)
    try:
        return recognizer.recognize_google(audio)
    except Exception:
        print("Skipping error")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )

    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Say hello to record thy question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transription = recognizer.recognize_google(audio)
                if transription == "hello":
                    filename = "input.wav"
                    with sr.Microphone as source:
                        print("State your question")
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        print("You said")

                        response = generate_response(text)
                        speak_text(response)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
