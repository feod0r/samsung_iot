import math
import time
import paho.mqtt.client as mqtt


class Coordinates():
	def __init__(self):
		self.ant_lat = 0
		self.ant_long = 0
		self.ant_height = 0
		self.sat_lat = 0
		self.sat_long = 0
		self.sat_height = 0
		self.teta = 0
		self.fi_priv = 0

		

	def transmit(self):

		R = 6371000;

		lat_ant = self.ant_lat
		lon_ant = self.ant_long

		h_ant = R + self.ant_height

		x_ant = h_ant * math.sin( lat_ant ) * math.cos( lon_ant );
		y_ant = h_ant * math.sin( lat_ant ) * math.sin( lon_ant );
		z_ant = h_ant * math.cos( lat_ant );

		h_sput = R + self.sat_height;

		lat_sput = self.sat_lat;
		lon_sput = self.sat_long;

		x_sput = h_sput * math.cos( lat_sput ) * math.cos( lon_sput );
		y_sput = h_sput * math.cos( lat_sput ) * math.sin( lon_sput );
		z_sput = h_sput * math.sin( lat_sput );

		x_sput_new = x_sput - x_ant;
		y_sput_new = y_sput - y_ant;
		z_sput_new = z_sput - z_ant;

		r = math.sqrt( x_sput_new ** 2 + y_sput_new ** 2 + z_sput_new**2 );

		if ( r > 0 ):
			teta = math.acos( z_sput_new / r );
		else:
			teta = 90.0;

		if ( x_sput_new > 0 ):
			fi = math.atan( y_sput_new / x_sput_new );
		else:
			fi = 0.0;
			
		teta = teta * 180.0 / math.pi;
		teta = 180 - teta
		fi   = teta * 180.0 / math.pi;

		#print ( teta );

		fi_priv = fi;

		if ( teta > 180 ):
			teta -= 180

		while ( fi_priv > 360 ):
			fi_priv -= 360;
			
		if ( fi_priv > 180 ):
			fi_priv -= 180

		#print( fi_priv );
		self.teta = teta
		self.fi_priv = fi_priv


		return teta, fi_priv



class PublicLora():
	def __init__(self, teta, fi_priv):
		self.client = mqtt.Client()
		self.client.connect("10.11.162.226", 1883, 60)
		self.client.publish("devices/lora/807B85902000022E/pwm",'set freq 970 dev 02 on ch 01 duty {}"'.format(teta),qos=0,retain=False)
		time.sleep(0.25)
		self.client.publish("devices/lora/807B85902000022E/gpio",'set 16 1',qos=0,retain=False)
		time.sleep(0.25)
		self.client.publish("devices/lora/807B85902000022E/pwm",'set freq 970 dev 02 on ch 01 duty {}"'.format(fi_priv),qos=0,retain=False)
		time.sleep(0.25)
		self.client.publish("devices/lora/807B85902000022E/gpio",'set 16 0',qos=0,retain=False)
		time.sleep(0.25)















	