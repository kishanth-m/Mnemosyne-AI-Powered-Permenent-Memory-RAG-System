from piper import PiperVoice
import sounddevice as sd
import numpy as np
import wave
import io

# Load voice model
voice = PiperVoice.load("voice/en_US-kristin-medium.onnx")

text = "Hello! I am your AI assistant. How are you doing today?"

# Generate WAV in memory
audio_buffer = io.BytesIO()

with wave.open(audio_buffer, "wb") as wav_file:
    voice.synthesize_wav(text, wav_file)

# Read WAV from memory
audio_buffer.seek(0)

with wave.open(audio_buffer, "rb") as wav_file:
    sample_rate = wav_file.getframerate()
    channels = wav_file.getnchannels()
    frames = wav_file.readframes(wav_file.getnframes())

# Convert to numpy
audio = np.frombuffer(frames, dtype=np.int16)

if channels > 1:
    audio = audio.reshape(-1, channels)

# Play directly through speakers
sd.play(audio, sample_rate)
sd.wait()

print("Finished speaking!")