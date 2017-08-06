#!/usr/bin/python
# encoding: utf-8

# license: MIT

# Raspberry Pi-powered cat feeder
# Ryan Matthews
# mhaddy@gmail.com

import schedule
import time
import datetime
import logging
import RPi.GPIO as GPIO
from twython import Twython
import configvars as cv

logging.basicConfig(filename=cv.log_dir+cv.log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# Twython
APP_KEY = cv.APPKEY
APP_SECRET = cv.APPSECRET
OAUTH_TOKEN = cv.ACCESSTOKEN
OAUTH_TOKEN_SECRET = cv.ACCESSTOKENSECRET

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

logging.info('----------------------------')
logging.info('Manually initiated FeedGoo routine for {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")))

GPIO.setmode(GPIO.BCM)

GPIO.setup(cv.servo_pin, GPIO.OUT)
GPIO.setup(cv.buzz_pin, GPIO.OUT)
GPIO.setup(cv.butt_switch_pin, GPIO.IN)
GPIO.setup(cv.butt_led_pin, GPIO.OUT)

GPIO.output(cv.buzz_pin, False)
GPIO.output(cv.butt_led_pin, False)

# Functions that make the world, err, feeder wheels go 'round

# Rotate feeder wheel clockwise
def servo_cw():
	servo = GPIO.PWM(cv.servo_pin, 50)
	servo.start(cv.rotate_time_cw)
	time.sleep(2)
	servo.stop()

# Rotate feeder wheel counter clockwise
# I'm not really using this right now but it will come in handy if the wheel
# gets stuck - so I'm keeping it here for now ... code to be updated at a
# later date to take advantage of this
def servo_ccw():
	servo = GPIO.PWM(cv.servo_pin, 50)
	servo.start(cv.rotate_time_ccw)
	time.sleep(2)
	servo.stop()

# Call the appropriate servo_XXX function
def feed_goo():
	#not yet implemented
	#GPIO.output(butt_led_pin, False)
	
	for x in range(0,10):	
		GPIO.output(cv.buzz_pin, True)
		time.sleep(.25)
		GPIO.output(cv.buzz_pin, False)

	#not yet implemented
	#GPIO.output(butt_led_pin, True)
	
	if cv.direction == "cw":
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
	logging.info("Goo has been manually fed! /{}".format(cv.direction))
	twitter.update_status(status="Goo has been manually fed! /{}".format(cv.direction))

manual_feed()
