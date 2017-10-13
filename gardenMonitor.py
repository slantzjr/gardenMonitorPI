#!/usr/bin/env python

"""A script to protect my plants when I'm gone"""

import RPi.GPIO as GPIO
from gardenMonitorEmail import gardenEmail
from gardenMonitorHTTP import gardenMonitorSession
from gardenThermometer import thermometer
from lightIntensity import lightMeasurement 
import time

GPIO_MOISTURE_IN = 26
GPIO_RELAY_PUMP_OUT = 17 
session = gardenMonitorSession.gardenMonitorSession()
session.login()

print 'Setting up GPIO'
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_MOISTURE_IN, GPIO.IN)
GPIO.setup(GPIO_RELAY_PUMP_OUT, GPIO.OUT)
GPIO.output(GPIO_RELAY_PUMP_OUT,0)
print 'GPIO setup complete'

pumpOutput = 1

while True:
  hasWater = GPIO.input(GPIO_MOISTURE_IN) == 0

  # If the pipe is dry fill it up
  while hasWater == False:
    if pumpOutput == 1:
      pumpOutput = 0
      GPIO.output(GPIO_RELAY_PUMP_OUT, pumpOutput)
    hasWater = GPIO.input(GPIO_MOISTURE_IN) == 0
    time.sleep(10)

  # Pipe should be full, turn pump off
  pumpOutput = 1
  GPIO.output(GPIO_RELAY_PUMP_OUT, pumpOutput)
 
  # Now we can take a measurement   
  temp = thermometer.read()
  lightIntensity = lightMeasurement.readLight()  
  session.login()
  session.sendMeasurement(temp, hasWater, lightIntensity)
  session.logout()
  
  time.sleep(600)
