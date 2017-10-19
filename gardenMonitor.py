#!/usr/bin/env python

"""A script to protect my plants when I'm gone"""

import RPi.GPIO as GPIO
from gardenMonitorEmail import gardenEmail
from gardenMonitorHTTP import gardenMonitorSession
from gardenThermometer import thermometer
from lightIntensity import lightMeasurement 
import time

GPIO_MOISTURE_IN = 26
GPIO_MOISTURE_OUT = 27
GPIO_RELAY_PUMP_OUT = 17 

# Relays operate backward (off = switch closed)
GPIO_OUT_OFF = 0
GPIO_OUT_ON = 1

try:
  session = gardenMonitorSession.gardenMonitorSession()
except:
  print "Failed to get session, data will not be sent"

def getHasWater():
  GPIO.output(GPIO_MOISTURE_OUT, GPIO_OUT_ON)
  time.sleep(1)
  hasWater = GPIO.input(GPIO_MOISTURE_IN) == 0
  GPIO.output(GPIO_MOISTURE_OUT, GPIO_OUT_OFF)
  return hasWater

print 'Setting up GPIO'
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_MOISTURE_IN, GPIO.IN)
GPIO.setup(GPIO_MOISTURE_OUT, GPIO.OUT)
GPIO.setup(GPIO_RELAY_PUMP_OUT, GPIO.OUT)
GPIO.output(GPIO_RELAY_PUMP_OUT, GPIO_OUT_ON)
print 'GPIO setup complete'

pumpOutput = GPIO_OUT_OFF

try:
  while True:
    try:
      hasWater = getHasWater() 

      # If the pipe is dry fill it up
      while hasWater == False:
        if pumpOutput == GPIO_OUT_ON:
          pumpOutput = GPIO_OUT_OFF
          GPIO.output(GPIO_RELAY_PUMP_OUT, pumpOutput)
        hasWater = getHasWater()
        time.sleep(10)

      # Pipe should be full, turn pump off
      pumpOutput = GPIO_OUT_ON
      GPIO.output(GPIO_RELAY_PUMP_OUT, pumpOutput)

      # Now we can take a measurement   
      temp = thermometer.read()
      lightIntensity = lightMeasurement.readLight()  

      # Then try to submit it to the site 
      try:
        session.login()
        session.sendMeasurement(temp, hasWater, lightIntensity)
        session.logout()
      except:
        print "Failed to send data point"

      time.sleep(600)
    except Exception as inst:
      print inst
      time.sleep(10)
except KeyboardInterrupt:
  print "Interrupt recieved, cleaning up gpio"
  GPIO.cleanup()
