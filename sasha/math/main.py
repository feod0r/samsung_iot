import math

R = 6371000;

lat_ant = 55.0;
lon_ant = 37.0;

h_ant = R + 100;

x_ant = h_ant * math.sin( lat_ant ) * math.cos( lon_ant );
y_ant = h_ant * math.sin( lat_ant ) * math.sin( lon_ant );
z_ant = h_ant * math.cos( lat_ant );

h_sput = R + 30000;

lat_sput = 55.753960;
lon_sput = 37.620393;

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
fi   = teta * 180.0 / math.pi;

print ( teta );

fi_priv = fi;

while ( fi_priv > 360 ):
	fi_priv -= 360;
	
print( fi_priv );
