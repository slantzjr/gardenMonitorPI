#!/usr/bin/env python

"""A script to protect my plants when I'm gone"""

import RPi.GPIO as GPIO
from gardenMonitorEmail import gardenEmail
from gardenMonitorHTTP import gardenMonitorSession
from gardenThermometer import thermometer
from lightIntensity import lightMeasurement 
import time

session = gardenMonitorSession.gardenMonitorSession()
session.login()

print 'Setting up GPIO'
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
print 'GPIO setup complete'

prevWater = True
while True:
  temp = thermometer.read()
  hasWater = GPIO.input(26) == 0
  lightIntensity = lightMeasurement.readLight()  
  session.sendMeasurement(temp, hasWater, lightIntensity)
  
  if hasWater != prevWater:
    gardenEmail.send_alert(hasWater)
  prevWater = hasWater
  time.sleep(600)
