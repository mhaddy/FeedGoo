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
from random import randint

logging.basicConfig(filename=cv.log_dir+cv.log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# we're using randint() here to prevent Twitter deleting tweets it feels are duplicates

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
	
	logging.debug("Servo rotate CW start")
	servo_cw()
	logging.debug("Servo rotate CW finish")

# TODO: Hook this into IFTTT
def manual_feed():
	feed_goo()
	logging.info("Goo has been manually fed!")
	twitter.update_status(status="Goo has been manually fed! /{}".format(randint(0,10000)))

manual_feed()
