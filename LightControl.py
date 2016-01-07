#!/usr/bin/python

import milight
import time

controller = ""
light = ""

controller = milight.MiLight({'host': '10.7.127.226', 'port': 8899}, wait_duration=.5)
light = milight.LightBulb(['rgbw', 'white', 'rgb'])

def initLights():

    print "Light Controller v0.1. Made by Yashi Sharma"
    print "Using McSwindler's python-milight library"

    controller.send(light.color(milight.color_from_rgb(255, 0, 0), 0))
    controller.send(light.color(milight.color_from_rgb(0, 255, 0), 0))
    controller.send(light.color(milight.color_from_rgb(0, 0, 255), 0))
    controller.send(light.white(0))
    controller.send(light.all_off())

def testLights():
    print "Starting test sequence. Looping through all the colors possible"
    for val in range(0,255):
            controller.send(light.color(val))
            print(val)

def setColor(r, g, b, bulb):
    controller.send(light.color(milight.color_from_rgb(r, g, b), bulb))

def setBrightness(val, led):
    controller.send(light.brightness(val, led))

def turnOn(led):
    controller.send(light.on(led))

def turnOff(led):
    controller.send(light.off(led))

def setHexColor(color, led):
    controller.send(light.color(milight.color_from_hex(color), led))
