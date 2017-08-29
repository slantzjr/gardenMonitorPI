def read():
	temperaturePath = "/sys/bus/w1/devices/28-0516a02db9ff/w1_slave"
	f = open(temperaturePath)
	text = f.read()
	temperature_data = text.split()[-1]
	temperature = float(temperature_data[2:])
	temperature = temperature / 1000
	f_temperature = cToF(temperature)
	return f_temperature

def cToF(temperature):
	return temperature * (9.0/5.0) + 32


