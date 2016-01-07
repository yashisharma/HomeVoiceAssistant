#!/usr/bin/env python

import apiai
import resampler as rs
import VAD as voicead
import pyaudio
import audioop
import time
import json
import urllib2
import requests
from pygame import mixer
import pyvona
import Commands
import threading


CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 192000
RECORD_SECONDS = 3

CLIENT_ACCESS_TOKEN = open("/APIKEYS/api.ai/ClientAccess.token").readline().rstrip()
SUBSCRIPTION_KEY =  open("/APIKEYS/api.ai/ClientAccess.token").readline().rstrip()

pyau = pyaudio.PyAudio();
mixer.init()
v = pyvona.create_voice('GDNAJ4XSWJBHSHA3AONA', 'AcSaGNHdlR290pxhawml89VpORQSmMz5/0RN19Ao')
v.voice_name = "Amy"
v.speech_rate = 'fast'
v.sentence_break = 200

def recordAndUpload(p):
	resampler = rs.Resampler(source_samplerate=RATE)

	vad = voicead.VAD()

	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)

	request = ai.voice_request()

	request.lang = 'en' # optional, default value equal 'en'

	def callback(in_data, frame_count, time_info, status):
		frames, data = resampler.resample(in_data, frame_count)
		state = vad.processFrame(frames)
		request.send(data)
		if (state == 1):
			return in_data, pyaudio.paContinue
		else:
			return in_data, pyaudio.paComplete

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					output=False,
					frames_per_buffer=CHUNK,
					stream_callback=callback)

	stream.start_stream()

	try:
		while stream.is_active():
			time.sleep(0.1)
	except Exception:
		raise e

	stream.stop_stream()
	stream.close()

	print("\tDone Listening...")
	print("\tGetting Results...")

	response = request.getresponse()
	responseParsed=response.read()
	results = json.loads(responseParsed)['result']
	resultParsed = results['resolvedQuery']
	outspeech = results['fulfillment']['speech']

	outputDict = dict([('parsedText', resultParsed), ('responseText', outspeech)])

	return outputDict

def query(output):
	try:
		parsed = output['parsedText']
		response = output['responseText']
	except Exception:
		parsed = ""
		response = ""
		print('TypeError' + output)

	print("\t\t"+parsed)

	if not parsed.find("mary") == -1:
		query = parsed.replace("mary", "")
		print "\t\t"+query
		ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)
		request = ai.text_request()
		request.lang = 'en'
		request.query = query
		response = request.getresponse()
		response = response.read()

                try:
			speechResponse = json.loads(response)['result']['fulfillment']['speech']
			action = json.loads(response)['result']['action']
			parameter = json.loads(response)['result']['parameters']
                        print "\t\t"+speechResponse
                        print "\t\t"+action
                        for key,value in parameter.items():
                            print "\t\t"+key+":"+value

		except Exception:
			response = ""
                        print "\t\tJSON response failure"


                if len(response)>1:
                    speak(speechResponse)
                    Commands.ParseInput(action, parameter)
		else:
	            playAudio("Speech Misrecognition.wav")
        print("\tDone Processing")

def playAudio(filename):
        mixer.music.load(filename)
        mixer.music.play()

def speak(text):
        playAudio("Speech On.wav")
        v.speak(text)
        playAudio("Speech Off.wav")

while True:
	print("Listening...")
        output = recordAndUpload(pyau);
	print("\tProcessing...")
	query(output)
