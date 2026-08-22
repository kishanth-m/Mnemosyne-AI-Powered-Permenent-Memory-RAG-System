import pyttsx3

def speak(word):

    # voice output Engine initialization
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    
    engine.setProperty("rate", 180)   # default is usually around 200
    engine.setProperty("volume", 1.0)
    engine.say(word)
    engine.runAndWait()


# speak("Hello, I am your AI assistant. How can I help you today?")