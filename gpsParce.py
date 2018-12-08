# -*- coding: utf-8 -*-
import pynmea2
import paho.mqtt.client as mqtt
import json
import requests
import subprocess
import time


class PublicLora():
	def __init__(self, teta, fi_priv):
		self.client = mqtt.Client()
		self.client.connect("10.11.162.226", 1883, 60)
		self.client.publish("devices/lora/807B85902000022E/pwm",'set freq 970 dev 02 on ch 01 duty {}"'.format(teta),qos=0,retain=False)
		time.sleep(0.5)
		self.client.publish("devices/lora/807B85902000022E/gpio",'set 16 1',qos=0,retain=False)
		time.sleep(0.5)
		self.client.publish("devices/lora/807B85902000022E/pwm",'set freq 970 dev 02 on ch 01 duty {}"'.format(fi_priv),qos=0,retain=False)
		time.sleep(0.5)
		self.client.publish("devices/lora/807B85902000022E/gpio",'set 16 0',qos=0,retain=False)
		time.sleep(0.5)
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("hyrocopter/devices/gps")
    



# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
	print(msg.payload)
	try:
		data = msg.payload.decode('UTF-8')
		
	except:
		print("Не встречены данные, пакет не относится к нам")
	else:	
		try:
			if data.find("$GPGGA") != -1:
				try:
					print(data)
				except Exception as e:
					print("2")
				gpgga = pynmea2.parse(data)

				alt = float(gpgga.altitude)
				lat = float(gpgga.lat)/100
				lon = float(gpgga.lon)/100

				r = requests.post("http://localhost:5000/sat_coord_json", data={'sat_lat': lat, 'sat_long': lon, 'sat_height' : alt})

				# r = requests.post("http://localhost:5000/sat_coord", data={'sat_lat': float(gpgga.lat)/100, 'sat_long': float(gpgga.lon)/100, 'sat_height' : float(gpgga.altitude)})
				print("alt ", alt)
				print("long", lon)
				print("lat ", lat)

				print(r.text)
				json_data = json.loads(r.text)


				try:
					LoraRun = PublicLora(json_data['teta'],json_data['fi_priv'])
					# returned_output = subprocess.check_output('mosquitto_pub -h "10.11.162.226" -t "devices/lora/807B85902000022E/pwm" -m "set freq 970 dev 02 on ch 01 duty {}"'.format(json_data['teta']))
					# returned_output = subprocess.check_output('mosquitto_pub -h "10.11.162.226" -t "devices/lora/807B85902000022E/gpio" -m "set 16 1"')

					# returned_output = subprocess.check_output('mosquitto_pub -h "10.11.162.226" -t "devices/lora/807B85902000022E/pwm" -m "set freq 970 dev 02 on ch 01 duty {}"'.format(json_data['fi_priv']))
					# returned_output = subprocess.check_output('mosquitto_pub -h "10.11.162.226" -t "devices/lora/807B85902000022E/gpio" -m "set 16 0"')
				except Exception as e:
					print(e)
				




				# client.publish("devices/lora/807B859020000260/gpio",'set 16 1',qos=0,retain=False)
				# client.publish("devices/lora/807B859020000260/gpio",'set 16 0',qos=0,retain=False)
			else: 
				print('не GPGGA!')
		except Exception as e:
			print("ошибка при обработке сообщения")
			



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.11.162.229", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# for x in range(0,10):
	# client.publish("mytopic",'Ya rodilsya',qos=0,retain=False)

client.loop_forever()



