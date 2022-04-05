# Code for an animatronic crow with two servo motors and a speaker connected to a Raspberry Pi headphone jack.
#
# When choosing a power cord for raspberry pi, check voltage (5v) but also amps: it appears 0.7 is too low
# when servos are involved (board will shut down on AngularServo calls below)
#
#
# 'To reduce servo jitter, use the pigpio pin factory.'
# See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# RUN DAEMON -> $> sudo pigpiod
#
# also has a service that can be started: systemtl enable pigpiod
#

import time
import datetime
from logger import logger

from crow import *

# Determine how many times to caw for current hour, then caw or not
#
# @param earliest_hour [Integer] default: 7 earlier hours won't be cawed
# @return [Nil]
def hour_callback(crow, earliest_hour=7):
    hour = datetime.datetime.now().hour
    # do not caw before 7am
    if hour >= earliest_hour:
        # convert 24-hr time to 12-hr
        if hour > 12:
            hour = hour - 12
        crow.rotate_caw_times('left', hour)


# Start blocking loop that runs hour_callback at the top of the hour
#
# @param crow [Crow] crow object
# @return [Nil]
def wait_for_hour(crow):
    while True:
        minute = datetime.datetime.now().minute
        logger.info(f"checking time, it's {minute}")
        if minute == 0:
            hour_callback(crow)
        # if minute % 10 == 0:
        #     logger.info(f"surprising because it's {minute}")
        #     crow.surprise()
        time.sleep(60)


if __name__ == '__main__':
    logger.info(f'Starting Crow Friend. Cawing on the Hour :)')
    crow = Crow()
    # crow.surprise()
    # begin waiting for hour
    wait_for_hour(crow)
