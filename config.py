import pyttsx3

text_to_speech = pyttsx3.init()

user_input = 'hi there'

text = 'hi there'
voices = text_to_speech.getProperty('voices')
text_to_speech.setProperty('voice', voices[1].id)

text_to_speech.say(text)
text_to_speech.runAndWait()