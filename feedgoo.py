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
from astral import *
from pytz import timezone

# lat/lon for sunset/sunrise calcs
# TODO: Use the geocoder for Toronto https://pythonhosted.org/astral/
city_name = 'Buffalo' # closest US city to Toronto that Astral supports
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
timezone = city.timezone
sun = city.sun(date=datetime.date(2009, 4, 22), local=True)

log_dir = "./logs"
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

