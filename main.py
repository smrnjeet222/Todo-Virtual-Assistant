import sys

import pyttsx3 as tts
import speech_recognition
from neuralintents import GenericAssistant

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ["Go shopping", "Go Code", "clean Room"]


def create_note():
	global recognizer

	speaker.say("What do you want to write onto your note?")
	speaker.runAndWait()

	done = False

	while not done:
		try:
			with speech_recognition.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				note = recognizer.recognize_google(audio).lower()

				speaker.say("Choose a filename!")
				speaker.runAndWait()

				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				filename = recognizer.recognize_google(audio)

			with open(filename, 'w') as f:
				f.write(note)
				done = True
				speaker.say(f"I successfully created the note {filename}")
				speaker.runAndWait()

		except speech_recognition.UnknownValueError:
			recognizer = speech_recognition.Recognizer()
			speaker.say("I didn't understant you! Please try again!")
			speaker.runAndWait()


def add_todo():
	global recognizer

	speaker.say("What do you want to add?")
	speaker.runAndWait()

	done = False

	while not done:
		try:
			with speech_recognition.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration=0.2)
				audio = recognizer.listen(mic)

				item = recognizer.recognize_google(audio).lower()
				todo_list.append(item)
				done = True

				speaker.say('I added the item in to do list!')
				speaker.runAndWait()

		except speech_recognition.UnknownValueError:
			recognizer = speech_recognition.Recognizer()
			speaker.say("I didn't understant you! Please try again!")
			speaker.runAndWait()


def show_todos():
	speaker.say('The items on your to do list are ')
	for item in todo_list:
		speaker.say(item)
	speaker.runAndWait()


def greetings():
	speaker.say('Hello, what can I do for you?')
	speaker.runAndWait()


def quit():
	speaker.say("Bye")
	speaker.runAndWait()
	sys.exit(0)


mappings = {
	'greeting': greetings,
	'create_note': create_note,
	'add_todo': add_todo,
	'show_todos': show_todos,
	'goodbye': quit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

assistant.save_model()

while True:
	try:
		with speech_recognition.Microphone() as mic:
			recognizer.adjust_for_ambient_noise(mic, duration=0.2)
			audio = recognizer.listen(mic)

			message = recognizer.recognize_google(audio).lower()

		assistant.request(message)

	except speech_recognition.UnknownValueError:
		recognizer = speech_recognition.Recognizer()
