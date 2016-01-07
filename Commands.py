import LightControl
import webcolors
import serial

arduino = serial.Serial('/dev/ttyACM1', 9600)

def ParseInput(action, parameter):
    if(action == "lights.power"):
        LightPower(parameter)
    if(action == "lights.color"):
        LightColor(parameter)
    if(action == "lights.brightness"):
        LightBrightness(parameter)
    if(action == "power.toggle"):
        OutletPower(parameter)

def LightPower(par):
    if(par['power-status'] == "On"):
        LightControl.turnOn(0)
    if(par['power-status'] == "Off"):
        LightControl.turnOff(0)

def LightColor(par):
    try:
        hexColor = webcolors.name_to_hex(par['color'])
    except Exception:
        hexColor = "#FFFFFF"
    LightControl.setHexColor(hexColor, 0)

def LightBrightness(par):
    LightControl.setBrightness(int(par['num']), 0)

def OutletPower(par):
    if(par['status'] == "on"):
        if(par['outlet'] == "1"):
            arduino.write(b'11')
        if(par['outlet'] == "2"):
            arduino.write(b'21')
        if(par['outlet'] == "3"):
            arduino.write(b'31')
        if(par['outlet'] == "4"):
            arduino.write(b'41')
        if(par['outlet'] == "5"):
            arduino.write(b'51')
    if(par['status'] == "off"):
        if(par['outlet'] == "1"):
            arduino.write(b'10')
        if(par['outlet'] == "2"):
            arduino.write(b'20')
        if(par['outlet'] == "3"):
            arduino.write(b'30')
        if(par['outlet'] == "4"):
            arduino.write(b'40')
        if(par['outlet'] == "5"):
            arduino.write(b'50')
