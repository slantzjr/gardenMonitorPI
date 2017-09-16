import json
import os
import requests

class gardenMonitorSession:
	coreURL = 'http://garden-monitor.herokuapp.com/'
	
	def __init__(self):
		self.request = requests.get(self.coreURL + "csrfToken")
		self.csrf = json.loads(self.request.text)['_csrf']
		
	def login(self):
		print "logging into website"
		loginData = {
			'email': os.environ['GARDEN_MONITOR_ADMIN_EMAIL'], 
			'password': os.environ['GARDEN_MONITOR_ADMIN_PASS'], 
			'_csrf': self.csrf}
		loginRequest = requests.put(self.coreURL + "login", data=loginData, cookies=self.request.cookies)
		print loginRequest.text

	def logout(self):
		logoutData = {
			'_csrf': self.csrf}
		logoutRequest = requests.put(self.coreURL + "logout", data=logoutData, cookies=self.request.cookies)
		print logoutRequest.status_code

	def sendMeasurement(self, temperature, hasWater, lightIntensity):
		measurementData = {
                    'temperature': "%.1f" % temperature, 
                    'hasWater': repr(hasWater).lower(), 
                    'lightIntensity': "%.1f" % lightIntensity, 
                    '_csrf': self.csrf
                }
                print "%.1f" % lightIntensity
                createMeasurementRequest = requests.put(self.coreURL + 'measurement', data=measurementData, cookies=self.request.cookies)
		print(measurementData)
		print(createMeasurementRequest.url)
		print(createMeasurementRequest.status_code)

