# HomeVoiceAssistant

I used a number of libraries:
https://github.com/api-ai/api-ai-python
  VAD.py
  __init__.py
  apiai.py
  resampler.py
https://github.com/McSwindler/python-milight

If I forgot to credit you, please send me a message so I can add you!

Current state: 
  1 Totally uncommented. Sorry guys! I'll work on that
  2 The program runs well, and detects/processes audio correctly most of the time. Need to work on accuracy a bit.
  3 It should work with any audio backend. I've tested it on Alsa and pulse, as well as a little work with JACK. Just change the audio device in pyVoicePoll.py
  4 I also have a program that controls the lighting on my Logitech g910 keyboard based off of voice recognition status, so I always have a monitor for what the program is doing. That is using simple UDP communication between the two computers. 


Feature todo list:
  Pet manager
    Automated feeding using a Petsafe feeder and some RF modules and a few custom built ATTiny85 boards that I have yet to print or design
    Cat litter ammonia detector
      Monitor ammonia levels of litter box and sound an alarm if it is too high
  Security - Door/window monitors using 433 MHz door sensors and an arduino
  Automatic control
    Sense if someone is in the apartment and turn on/off lights based on that info
    Turn on espresso machine in the morning
    Set lights to red at night, blue in the morning
    Plant watering
  Nest thermostat control
  Air quality monitor
  Percipitation meter
  Laundry machine alerts
    Possibly using piezos and another 433MHz transmitter/reciever (I already have the network going, may as well use it
  More lighting effects for the keyboard.
    Escape key as voice monitor/processing indicator
    Change color based on lighting
    
Other todo:
  I really need a better mic. I'm just using a pair of PS3 Eyes right now. They're good, but not great/
    Looking into the ICE omnidirectional Mic
  Recode some of the librares that I am using so that I can customize them to my liking.
  Make some kind of a control panel. 
    I'm thinking about using a 7 in touchscreen display with a few angel eyes and rgb leds along the sides to be aestheticly pleasing as well as giving some insight into the status of the program.
