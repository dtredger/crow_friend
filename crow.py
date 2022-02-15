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
import threading

import gpiozero
from gpiozero import AngularServo
import time
from time import sleep
import datetime

import pygame
from audio import *

from gpiozero.pins.pigpio import PiGPIOFactory
gpiozero.Device.pin_factory = PiGPIOFactory()


# def setup():
print("setup crow friend")
SOUND_FILE_ROOT = '/home/pi/crow_friend/sounds/'
WOOW_X = 'woow_x.wav'
SURPRISE = 'surprise.mp3'
SURPRISE_L = 'surprise_louder.mp3'
# 1 Caw, 700ms
CAW_1  = 'crow_1_loud.mp3'
# 4 caws, 3s
CAW_4 = 'crow_4.wav'
# Pi pins 24 & 25
BEAK_SERVO_PIN = 25
HEAD_SERVO_PIN = 24
# angles -90 -> +90
BEAK_SERVO = AngularServo(BEAK_SERVO_PIN, initial_angle=-90)
HEAD_SERVO = AngularServo(HEAD_SERVO_PIN)
# volume range from 0 to 1
pygame.mixer.init()
pygame.mixer.music.set_volume(1)


class Crow(object):
    """A Crow object is created and does things."""
    def __init__(self, arg):
        super(Crow, self).__init__()
        self.arg = arg
        # -90 = max closed;
        # 90 = max open (but ~30 is a good open-mouth maximum)
        self.HEAD_SERVO = AngularServo(BEAK_SERVO_PIN)
        self.BEAK_SERVO = AngularServo(HEAD_SERVO_PIN, initial_angle=-90)
        pygame.mixer.init()
        # volume range from 0 to 1
        pygame.mixer.music.set_volume(1)

    # Open beak and rotate one direction (L or R), then crow
    # rotation a little slow
def rotate_and_crow():
    slow_rotate_to(HEAD_SERVO, -90)
    caw_caw_caw()
    slow_rotate_to(HEAD_SERVO, 0)

def caw_caw_caw():
    open_mouth_for_sound(BEAK_SERVO, CAW_4, 2.5)

# Given a sound x seconds long, have the servo fully rotated (to its
# open_position) at time = x/2, and back at shut_position at time = x
def open_mouth_for_sound(servo, sound, time_s, shut_position=-90, open_position=30):
    start_time = time.time()
    slow_rotate_to(servo, open_position, interval=0.0001, speed_multiplier=5)
    play(sound)
    elapsed_time = time.time() - start_time
    # count two rotation times, and only sleep for the remaining time in time_s
    sleep(time_s - elapsed_time*2)
    slow_rotate_to(servo, shut_position, interval=0.0001, speed_multiplier=5)


# Open mouth a bit, rotate head, and stare without sound.
# Crows seem to do this sometimes.
def open_beak_rotate(beak_servo=BEAK_SERVO, head_servo=HEAD_SERVO):
    open_beak(beak_servo, max_open=30)
    slow_oscillate(head_servo)
    open_beak(beak_servo, max_open=-80)

# for example, with sleep time of 0.1 between each angle-set, the total
# time comes to 9.66 (so almost all the time is sleep: 90*0.1)
# a 0.01s sleep time gives a 90-degree rotation in 1.6 seconds
def slow_oscillate(servo, interval=0.01):
    slow_rotate_to(servo, 0)
    for angle in range(0,90):
        servo.angle = angle
        sleep(interval)
    for angle in range(90, -90, -1):
        servo.angle = angle
        sleep(interval)
    for angle in range(-90, 0):
        servo.angle = angle
        sleep(interval)

# In cases where the current servo position is not what is desired,
# slowly rotate to that position (to prevent violent jerk to the
# starting position in some other method)
def slow_rotate_to(servo, target_angle, interval=0.005, speed_multiplier=1):
    initial_angle = int(servo.angle)
    if target_angle > initial_angle:
        step = 1 * speed_multiplier
    else:
        step = -1 * speed_multiplier
    for angle in range(initial_angle, target_angle, step):
        servo.angle = angle

# max_open takes a value from -90 (beak shut) => +90)
# The beak appears fully open at +30
def open_beak(servo, max_open):
    initial_angle = -90
    interval = 0.03
    for ang in range(initial_angle, max_open):
        servo.angle = ang
        sleep(interval)

# play sound
def play(filename):
    full_path = SOUND_FILE_ROOT + filename
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()

def caw_x_times(times):
    # iterate through once fewer than `times`
    shut_position = -90
    for x in range(1, times):
        shut_position = 20
        open_mouth_for_sound(BEAK_SERVO, CAW_1, 1.0, shut_position, open_position=30)
    # last iteration shut all the way
    open_mouth_for_sound(BEAK_SERVO, CAW_1, 1.0, shut_position=-90, open_position=30)


def surprise(rotate_direction='left'):
    if rotate_direction == 'right':
        angle = -80
    else:
        angle = 80
    slow_rotate_to(HEAD_SERVO, angle)
    open_mouth_for_sound(BEAK_SERVO, SURPRISE_L, 2.0, -90, open_position=30)
    slow_rotate_to(HEAD_SERVO, 0)



# rotate_direction either `right` or not (left)
# The servo (appears to) struggle to reach 90 (and is noisy in
# the attempt, so cap at 80 rotation)
def rotate_caw_times(rotate_direction, times):
    if rotate_direction == 'right':
        angle = -80
    else:
        angle = 80
    slow_rotate_to(HEAD_SERVO, angle)
    caw_x_times(times)
    slow_rotate_to(HEAD_SERVO, 0)



# 3600s = 1hr
@set_interval(3600)
def hour_callback():
    print(f'hour_callback')
    hour = datetime.datetime.now().hour
    # do not caw before 7am
    if hour >= 7:
        if hour > 12:
            hour = hour - 12
            rotate_caw_times('left', hour)

# check once every 60s, max 60 times
@set_interval(60, 60)
def wait_for_hour():
    minute = datetime.datetime.now().minute
    print(f"checking time, it's {minute}")
    if minute == 0:
        hour_callback()





if __name__ == '__main__':
    # setup()
    print(f'Starting Crow Friend. Cawing on the Hour :)')
    wait_for_hour()
