# encoding: utf-8

# license: MIT

# Raspberry Pi-powered cat feeder
# Ryan Matthews
# mhaddy@gmail.com

import time
import datetime
from datetime import date, timedelta, datetime
import logging
import RPi.GPIO as GPIO
from astral import Astral
from pytz import timezone

# lat/lon for sunset/sunrise calcs
# TODO: Use the geocoder for Toronto https://pythonhosted.org/astral/
city_name = 'Buffalo' # closest US city to Toronto that Astral supports
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
time_zone = city.timezone
sun = city.sun(date=datetime.now(), local=True)

# logging
log_dir = "/var/log/feedgoo/"
log_filename = "feedgoo_"+datetime.now().strftime("%Y%m%d")+".log"

logging.basicConfig(filename=log_dir+log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)

logging.debug('Information for %s/%s\n' % (city_name, city.region))
logging.debug('Timezone: %s' % time_zone)
logging.debug('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
logging.debug('Dawn:    %s' % str(sun['dawn']))
logging.debug('Sunrise: %s' % str(sun['sunrise']))
logging.debug('Noon:    %s' % str(sun['noon']))
logging.debug('Sunset:  %s' % str(sun['sunset']))
logging.debug('Dusk:    %s' % str(sun['dusk']))

# GPIO setup
GPIO.setwarnings(False)

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
# https://circuitdigest.com/microcontroller-projects/raspberry-pi-servo-motor-control
rotate_time_cw = 6.5
rotate_time_ccw = 7.5

# Functions that make the world, err, feeder wheels go 'round

# Rotate feeder wheel clockwise
def servo_cw(servo_pin, rotate_time_cw):
	servo = GPIO.PWM(servo_pin, 50)
	servo.start(rotate_time_cw)
	time.sleep(1)
	servo.stop()
	time.sleep(1)

# Rotate feeder wheel counter clockwise
def servo_ccw(servo_pin, rotate_time_ccw):
	servo = GPIO.PWN(servo_pin, 50)
	servo.start(rotate_time_ccw)
	time.sleep(1)
	servo.stop()
	time.sleep(1)

# Call the appropriate servo_XXX function
def feed_goo(rotate_time_cw, rotate_time_ccw, direction):
	GPIO.output(butt_led_pin, False)
	GPIO.output(buzz_pin, True)
	time.sleep(.10)
	GPIO.output(buzz_pin, False)
	GPIO.output(butt_led_pin, True)
	
	logging.info("Dispensing food")

	if direction == "cw":
		logging.debug("Servo rotate CW start")
		servo_cw(servo_pin, rotate_time_cw)
		logging.debug("Servo rotate CW finish")
	else:
                logging.debug("Servo rotate CCW start")
                servo_ccw(servo_pin, rotate_time_ccw)
                logging.debug("Servo rotate CCW finish")

	time.sleep(60)

# If the push button is ... pushed, manually operate the feeder wheel
def manual_feed(servo_pin, rotate_time_cw=rotate_time_cw, rotate_time_ccw=rotate_time_ccw):
	feed_goo(rotate_time_cw, rotate_time_ccw, "cw")
	feeding_time = datetime.now()
	logging.info('Fed Goo at {}'.format(feeding_time))

def when_is_dusk():
	dusk = city.dusk(local=True, date=None)
	dusk2 = dusk.strftime("%Y-%m-%d %H:%M:%S")
	return dusk2

# Detect when the manual_feed button is pushed
#GPIO.add_event_detect(butt_switch_pin, GPIO.RISING, callback=manual_feed, bouncetime=500)

# Set the initial dusk time
dusk = when_is_dusk()
logging.info('I will feed Goo on {}'.format(dusk))

# Turn on button LED
#GPIO.output(butt_switch_led, True)

# Main program loop
while True:
	now = datetime.now().strftime("%Y-%m-%d %H:%M:S")
	
	if now == dusk:
		feeding_time = datetime.now()
		logging.info('Starting Goo Feed at {}'.format(feeding_time.strftime("%Y-%m-%d %H:%M:%S")))
		
		feed_goo(rotate_time_cw, rotate_time_ccw, "cw")

		logging.info('Finishing Goo Feed at {}'.format(feeding_time.strftime("%Y-%m-%d %H:%M:%S")))

		time.sleep(60)
	if time.strftime("%H") == "03" and time.strftime("%M") == "01" and time.strftime("%S") == "01":
		dusk = when_is_dusk()

	time.sleep(1)
