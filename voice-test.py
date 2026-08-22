import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

answer = "hi, i am your AI assistant! how can i help you today?"

engine.say(answer)
engine.runAndWait()