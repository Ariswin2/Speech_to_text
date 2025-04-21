import speech_recognition as sr
import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import warnings

# Suppress ALSA warnings (Linux) and other noise
warnings.filterwarnings("ignore")

def record_audio(filename, duration=15, sample_rate=44100):
    """Record audio and save as WAV file"""
    print(f"Recording for {duration} seconds...")
    try:
        # Record stereo audio
        audio_data = sd.rec(int(duration * sample_rate),
                          samplerate=sample_rate,
                          channels=2,
                          dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save as 16-bit WAV file
        write(filename, sample_rate, audio_data)
        print(f"Audio saved as {filename}")
        return True
    except Exception as e:
        print(f"Recording failed: {str(e)}")
        return False

def speech_to_text(audio_file):
    """Convert speech audio to text"""
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Processing audio...")

            # Record the audio data
            audio = recognizer.record(source)

            # Recognize using Google Web Speech API
            text = recognizer.recognize_google(audio)
            return text

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"API unavailable: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    OUTPUT_FILE = "recording.wav"

    # Step 1: Record audio
    if record_audio(OUTPUT_FILE):
        # Step 2: Convert to text
        print("Converting speech to text...")
        result = speech_to_text(OUTPUT_FILE)
        print("\nResult:", result)

        # Clean up (optional)
        try:
            os.remove(OUTPUT_FILE)
        except:
            pass
        