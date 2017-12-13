BROADCAST_TO_PORT = 11235
import RPi.GPIO as GPIO
import time
from subprocess import call
from socket import *

tempReadPpin = 2

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

import smbus
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    input_state=GPIO.input(23)
    if input_state == False:
        print("Button Pressed/Fridge Closed")
        time.sleep(0.2)
        print("LED On/Fridge Light On")
        GPIO.output(18,GPIO.HIGH)
        print("Taking Picture")
        call(['bash','takepicture.sh'])
        time.sleep(5)
        print("Picture Has Been Taken")
        print("LED Off/Fridge Light Off")
        GPIO.output(18, GPIO.LOW)
        print("Transfering picture To FTP Server")
        call(['bash','uploadToAzureServer.sh'])
        time.sleep(2)


    humidity, temperature = Adafruit_DHT.read_retry(sensor, tempReadPpin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        data = "%s"%(format(temperature))
        s.sendto(bytes(data, "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
        print(bytes(data,"UTF-8"))
    data = "%s"%(reading3)


GPIO.cleanup()
