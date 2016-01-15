#!/usr/bin/python

import sys
sys.path.insert(0, r'/root/HomeVoiceAssistant/lib')
import apiai
import resampler as rs
import VAD as voicead
import pyaudio
import audioop
import time
import json
#import rllib2
import requests
from pygame import mixer
import pyvona
import Commands
import threading
import socket

UDP_IP = "10.7.127.161"
UDP_PORT = 666
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3

CLIENT_ACCESS_TOKEN = open("/APIKEYS/api.ai/ClientAccess.token").readline().rstrip()
SUBSCRIPTION_KEY =  open("/APIKEYS/api.ai/ClientAccess.token").readline().rstrip()

pyau = pyaudio.PyAudio();
mixer.init()
v = pyvona.create_voice('GDNAJ4XSWJBHSHA3AONA', 'AcSaGNHdlR290pxhawml89VpORQSmMz5/0RN19Ao')
v.voice_name = "Amy"
v.speech_rate = 'medium'
v.sentence_break = 200
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def recordAndUpload(p):
	resampler = rs.Resampler(source_samplerate=RATE)

	vad = voicead.VAD()

	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)

	request = ai.voice_request()

	request.lang = 'en' # optional, default value equal 'en'

	def callback(in_data, frame_count, time_info, status):
		frames, data = resampler.resample(in_data, frame_count)
		state = vad.processFrame(frames)

                try:
                        request.send(data)
                except Exception:
                        textOut("Error sending data");
		if (state == 1):
			return in_data, pyaudio.paContinue
		else:
			return in_data, pyaudio.paComplete

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					output=False,
                                        input_device_index=3,
					frames_per_buffer=CHUNK,
					stream_callback=callback)

	stream.start_stream()

	try:
		while stream.is_active():
			time.sleep(0.1)
	except Exception:
                textOut("Error processing audio")
		raise e

	stream.stop_stream()
	stream.close()

	textOut("\tDone Listening...")
	textOut("\tGetting Results...")

        try:
            response = request.getresponse()
            responseParsed=response.read()
            results = json.loads(responseParsed)['result']
            resultParsed = results['resolvedQuery']
            outspeech = results['fulfillment']['speech']
        except Exception:
            resultParsed=""
            outspeech=""
            textOut("Error getting response")

	outputDict = dict([('parsedText', resultParsed), ('responseText', outspeech)])

	return outputDict

def query(output):
	try:
		parsed = output['parsedText']
		response = output['responseText']
	except Exception:
		parsed = ""
		response = ""
		textOut('Type Error ' + output)

	textOut("\t\t"+parsed)

	if not parsed.find("carry") == -1 or not parsed.find("karen") == -1 or not parsed.find("carrie") == -1:
		query = parsed.replace("carrie", "")
		query = query.replace("karen", "")
		query = query.replace("carry", "")
		textOut("\t\t"+query)
		ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)
		request = ai.text_request()
		request.lang = 'en'
		request.query = query
                try:
                    response = request.getresponse()
                    response = response.read()
                except Exception:
                    textOut("Response parsing Error")
                    response = -1

                if (not response==-1):
                    try:
			speechResponse = json.loads(response)['result']['fulfillment']['speech']
			action = json.loads(response)['result']['action']
			parameter = json.loads(response)['result']['parameters']
                        textOut("\t\t"+speechResponse)
                        textOut("\t\t"+action)
                        for key,value in parameter.items():
                            textOut("\t\t"+key+":"+value)
                    except Exception:
			response = ""
                        textOut ("\t\tJSON response Error")


                if len(response)>1:
                    speak(speechResponse)
                    Commands.ParseInput(action, parameter)
		else:
                    textOut("\t\tNo output Error")
                    playAudio("sound/Speech Misrecognition.wav")
        textOut("\tDone Processing")

def playAudio(filename):
        mixer.music.load(filename)
        mixer.music.play()

def speak(text):
        playAudio("sound/Speech On.wav")
        try:
            v.speak(text)
        except Exception:
            textOut("Error speaking")
        playAudio("sound/Speech Off.wav")

def textOut(text):
    print(text)
    sock.sendto(text,(UDP_IP, UDP_PORT))


#for i in range(0,10):
    #print pyau.get_device_info_by_index(i)
while True:
	textOut("Listening...")
        output = recordAndUpload(pyau);
	textOut("\tProcessing...")
	query(output)
