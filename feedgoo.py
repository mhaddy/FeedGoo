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
import pygame
import pygame.camera
from pygame.locals import *

logging.basicConfig(filename=cv.log_dir+cv.log_filename,format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# we're using randint() here to prevent Twitter deleting tweets it feels are duplicates

# Twython
APP_KEY = cv.APPKEY
APP_SECRET = cv.APPSECRET
OAUTH_TOKEN = cv.ACCESSTOKEN
OAUTH_TOKEN_SECRET = cv.ACCESSTOKENSECRET

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

logging.info('----------------------------')
logging.info('Beginning FeedGoo routine for {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")))
twitter.update_status(status="FeedGoo has been activated! /{}".format(randint(0,10000)))

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
	time.sleep(2)

        # take a picture 2 seconds after servo stops
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera('/dev/video0',(640,480))
        cam.start()
        image = cam.get_image()
        pygame.image.save(image,'/home/mhadpi/pics/image.jpg')
        photo = open('/home/mhadpi/pics/image.jpg','rb')

	response = twitter.upload_media(media=photo)
	twitter.update_status(status="Goo has been fed! /{}.{}".format(cv.direction,randint(0,10000)), media_ids=[response['media_id']])

# Rotate feeder wheel counter clockwise
# I'm not really using this right now but it will come in handy if the wheel
# gets stuck - so I'm keeping it here for now ... code to be updated at a
# later date to take advantage of this
def servo_ccw():
	servo = GPIO.PWM(cv.servo_pin, 50)
	servo.start(cv.rotate_time_ccw)
	time.sleep(2)
	servo.stop()
	time.sleep(2)

        # take a picture 2 seconds after servo stops
        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera('/dev/video0',(640,480))
        cam.start()
        image = cam.get_image()
        pygame.image.save(image,'/home/mhadpi/pics/image.jpg')
        photo = open('/home/mhadpi/pics/image.jpg','rb')

        response = twitter.upload_media(media=photo)
        twitter.update_status(status="Goo has been fed! /{}.{}".format(cv.direction,randint(0,10000)), media_ids=[response['media_id']])

# Call the appropriate servo_XXX function
def feed_goo():
	#not yet implemented
	#GPIO.output(cv.butt_led_pin, False)
	
	for x in range(0,10):	
		GPIO.output(cv.buzz_pin, True)
		time.sleep(.25)
		GPIO.output(cv.buzz_pin, False)

	#not yet implemented
	#GPIO.output(cv.butt_led_pin, True)
	
	if cv.direction == "cw":
		logging.debug("Servo rotate CW start")
		servo_cw()
		logging.debug("Servo rotate CW finish")
	else:
                logging.debug("Servo rotate CCW start")
                servo_ccw()
                logging.debug("Servo rotate CCW finish")

# If the push button is ... pushed, manually operate the feeder wheel
# not yet implemented
def manual_feed():
        feed_goo()
        logging.info("Goo has been manually fed! /{}".format(cv.direction))
        twitter.update_status(status="Goo has been manually fed! /{}.{}".format(cv.direction,randint(0,10000)))

# Detect when the manual_feed button is pushed
# not yet implemented
#GPIO.add_event_detect(cv.butt_switch_pin, GPIO.RISING, callback=manual_feed, bouncetime=500)

# Turn on button LED
# not yet implemented
#GPIO.output(cv.butt_switch_led, True)

# feeding schedule
# https://pypi.python.org/pypi/schedule
# TODO: use Astral/Pytz to find dawn/dusk and feed accordingly
# instead of hard-set times
schedule.every().day.at(cv.morningtime).do(feed_goo)
schedule.every().day.at(cv.eveningtime).do(feed_goo)

# Main program loop
while True:
	schedule.run_pending()
	time.sleep(30)
