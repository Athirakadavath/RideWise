import speech_recognition as sr
import os

def transcribe_audio(audio_file):
    """Transcribe audio to text"""
    try:
        recognizer = sr.Recognizer()

        temp_path = 'temp_audio.wav'
        audio_file.save(temp_path)

        with sr. AudioFile(temp_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        try:
            text = recognizer. recognize_google(audio_data)
            print(f"Transcribed text: {text}")

            if os.path.exists(temp_path):
                os.remove(temp_path)

            return text

        except sr. UnknownValueError:
            print("Could not understand audio")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None

        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None

    except Exception as e:
        print(f"Audio transcription error: {str(e)}")
        return None