# speak.py

from piper import PiperVoice
import sounddevice as sd
import numpy as np
import wave
import io

voice = PiperVoice.load("voice/en_US-amy-medium.onnx")

def speak(text):
    audio_buffer = io.BytesIO()

    with wave.open(audio_buffer, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    audio_buffer.seek(0)

    with wave.open(audio_buffer, "rb") as wav_file:
        rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        frames = wav_file.readframes(wav_file.getnframes())

    audio = np.frombuffer(frames, dtype=np.int16)

    if channels > 1:
        audio = audio.reshape(-1, channels)

    sd.play(audio, rate)
    sd.wait()