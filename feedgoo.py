# encoding: utf-8

# license: MIT

# Raspberry Pi-powered cat feeder
# Ryan Matthews
# mhaddy@gmail.com

import time
import datetime
import logging
import RPi.GPIO as GPIO
from astral import *
from pytz import timezone

# lat/lon for sunset/sunrise calcs
# TODO: Use the geocoder for Toronto https://pythonhosted.org/astral/
city_name = 'Buffalo' # closest US city to Toronto that Astral supports
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
time_zone = city.timezone
sun = city.sun(date=datetime.date(2009, 4, 22), local=True)

# logging
log_dir = "/var/log/feedgoo/"
log_filename = "feedgoo.log"

logging.basicConfig(filename=log_dir+log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)

logging.debug('Information for %s/%s\n' % (city_name, city.region))
logging.debug('Timezone: %s' % timezone)
logging.debug('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
logging.debug('Dawn:    %s' % str(sun['dawn']))
logging.debug('Sunrise: %s' % str(sun['sunrise']))
logging.debug('Noon:    %s' % str(sun['noon']))
logging.debug('Sunset:  %s' % str(sun['sunset']))
logging.debug('Dusk:    %s' % str(sun['dusk']))

# GPIO setup

servo_pin = 18 # servo
buzz_pin = 23 # buzzer
butt_switch_pin = 24 # button switch
butt_led_pin = 25 # button led

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(buzz_pin, GPIO.OUT)
GPIO.setup(butt_switch_pin, GPIO.IN)
GPIO.setup(butt_led_pin, GPIO.OUT)

GPIO.output(buzz_pin, False)
GPIO.output(butt_led_pin, False)

# How long should we rotate the feeder wheel (seconds)?
rotate_time = 1.3

# Functions that make the world, err, feeder wheels go 'round

# Rotate feeder wheel clockwise
def servo_cw(servo_pin, sleep_time):
	servo = GPIO.PWM(servo_pin, 50)
	servo.start(10.5)
	time.sleep(sleep_time)
	servo.stop()
	time.sleep(.05)

# Rotate feeder wheel counter clockwise
def servo_ccw(servo_pin, sleep_time):
	servo = GPIO.PWN(servo_pin, 50)
	servo.start(4.5)
	time.sleep(sleep_time)
	servo.stop()

# Call the appropriate servo_XXX function
def feed_goo(rotate_time, direction):
	GPIO.output(butt_led_pin, False)
	GPIO.output(buzz_pin, True)
	time.sleep(.10)
	GPIO.output(buzz_pin, False)
	GPIO.output(butt_led_pin, True)
	
	if direction == "cw":
		logging.info("Servo rotate CW start")
		servo_cw(servo_pin, rotate_time)
		logging.info("Servo rotate CW finish")
		time.sleep(.25)
	else:
                logging.info("Servo rotate CCW start")
                servo_ccw(servo_pin, rotate_time)
                logging.info("Servo rotate CCW finish")
                time.sleep(.25)

# Call the feeding routine if the hour and min match the settings
def feed_time(feed_hour, feed_min):
	if time.strftime("%H") == feed_hour and time.strftime("%M") == feed_min:
		logging.info("Dispensing food")
		feed_goo(rotate_time, "cw")
		time.sleep(60)

# If the push button is ... pushed, manually operate the feeder wheel
def manual_feed(servo_pin):
	feed_good(feeding_time, sleep_time)
	feed_time = datetime.now(time_zone)
	logging.info('Fed Goo at {}'.format(feed_time))

def when_is_dusk():
	dusk = location.dusk(local=True, date=None)
	dusk2 = dusk.strftime("%Y-%m-%d %H:%M:%S")
	return dusk2

# Detect when the manual_feed button is pushed
GPIO.add_event_detect(butt_switch_pin, GPIO.RISING, callback=manual_feed, bouncetime=500)

# Set the initial dusk time
dusk = when_is_dusk()
logging.info('I will feed Goo on {}'.format(dusk))

# Turn on button LED
#GPIO.output(butt_switch_led, True)

# Main program loop
while True:
	now = datetime.now().strftime("%Y-%m-%d %H:%M:S")
	
	if now == dusk:
		feed_time = datetime.now(time_zone)
		logging.info('Starting Goo Feed at {}'.format(feed_time.strftime("%Y-%m-%d %H:%M:%S"))
		
		feed_goo(rotate_time,"cw")

		logging.info('Finishing Goo Feed at {}'.format(feed_time.strftime("%Y-%m-%d %H:%M:%S"))

		time.sleep(60)
	if time.strftime("%H") == "03" and time.strftime("%M") == "01" and time.strftime("%S") == "01":
		dusk = when_is_dusk()
	time.sleep(1)
