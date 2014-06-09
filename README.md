


== setup ==

# apt-get install python-smbus

add the user that's going to run the code to group i2c, this avoids
having to run it as root:

# usermod -a -G i2c <user>

== notes ==

The sensor source code is here:

https://github.com/Miceuz/PlantWateringAlarm/blob/release/sensor/src/main.c

