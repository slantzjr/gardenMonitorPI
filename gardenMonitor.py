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
GPIO.setup(17, GPIO.OUT)
GPIO.output(17,0)
print 'GPIO setup complete'

pumpOutput = 1

while True:
  hasWater = GPIO.input(26) == 0

  # If the pipe is dry fill it up
  while hasWater == False:
    if pumpOutput == 1:
      pumpOutput = 0
      GPIO.output(17, pumpOutput)
    hasWater = GPIO.input(26) == 0
    time.sleep(10)

  # Pipe should be full, turn pump off
  pumpOutput = 1
  GPIO.output(17, pumpOutput)
 
  # Now we can take a measurement   
  temp = thermometer.read()
  lightIntensity = lightMeasurement.readLight()  
  session.login()
  session.sendMeasurement(temp, hasWater, lightIntensity)
  session.logout()
  
  time.sleep(600)
