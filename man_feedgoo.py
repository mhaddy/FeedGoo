#!/usr/bin/python
# encoding: utf-8

# license: MIT

# Raspberry Pi-powered cat feeder
# Ryan Matthews
# mhaddy@gmail.com

import schedule
import time
import datetime
#from datetime import date, timedelta, datetime
import logging
import RPi.GPIO as GPIO
#import pytz
#from pytz import timezone

# logging
log_dir = "/var/log/feedgoo/"

# if you want your logs to rotate, uncomment the below
# log_filename = "feedgoo_"+datetime.now().strftime("%Y%m%d")+".log"
log_filename = "feedgoo.log"

logging.basicConfig(filename=log_dir+log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)

logging.info('----------------------------')
logging.info('Beginning Feed Goo routine for {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")))

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

# How long should we rotate the feeder wheel (refers to duty cycle)?
# length of time for wheel rotation determined by time.sleep(x) following servo.start() cmd
# https://circuitdigest.com/microcontroller-projects/raspberry-pi-servo-motor-control
rotate_time_cw = 6.5
rotate_time_ccw = 7.5

direction = "ccw"

# Functions that make the world, err, feeder wheels go 'round

# Rotate feeder wheel clockwise
def servo_cw():
	servo = GPIO.PWM(servo_pin, 50)
	servo.start(rotate_time_cw)
	time.sleep(2)
	servo.stop()

# Rotate feeder wheel counter clockwise
# I'm not really using this right now but it will come in handy if the wheel
# gets stuck - so I'm keeping it here for now ... code to be updated at a
# later date to take advantage of this
def servo_ccw():
	servo = GPIO.PWM(servo_pin, 50)
	servo.start(rotate_time_ccw)
	time.sleep(2)
	servo.stop()

# Call the appropriate servo_XXX function
# TODO: incorporate the direction into the call; for now, it's cw
def feed_goo():
	#GPIO.output(butt_led_pin, False)
	
	for x in range(0,10):	
		GPIO.output(buzz_pin, True)
		time.sleep(.25)
		GPIO.output(buzz_pin, False)

	#GPIO.output(butt_led_pin, True)
	
	if direction == "cw":
		logging.debug("Servo rotate CW start")
		servo_cw()
		logging.debug("Servo rotate CW finish")
	else:
                logging.debug("Servo rotate CCW start")
                servo_ccw()
                logging.debug("Servo rotate CCW finish")

# If the push button is ... pushed, manually operate the feeder wheel
def manual_feed():
	feed_goo()
	feeding_time = datetime.datetime.now()
	logging.info('Manually fed Goo at {}'.format(feeding_time))


manual_feed()
