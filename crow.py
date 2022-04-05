import time

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory
gpiozero.Device.pin_factory = PiGPIOFactory()

import audio
from logger import logger

# Pi pins 24 & 25
BEAK_SERVO_PIN = 25
HEAD_SERVO_PIN = 24

class Crow(object):
    """
        Code for an animatronic crow with two servo motors and a speaker connected to a Raspberry Pi headphone jack.

        When choosing a power cord for raspberry pi, check voltage (5v) but also amps: it appears 0.7 is too low
        when servos are involved (board will shut down on AngularServo calls below)

        'To reduce servo jitter, use the pigpio pin factory.' See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
        RUN DAEMON -> $> sudo pigpiod (it is also a service that can be enabled)
    """

    def __init__(self, beak_pin=BEAK_SERVO_PIN, head_pin=HEAD_SERVO_PIN, sound_module=audio):
        # -90 = max closed;
        # 90 = max open (but ~30 is a good open-mouth maximum)
        self.HEAD_SERVO = gpiozero.AngularServo(beak_pin)
        self.BEAK_SERVO = gpiozero.AngularServo(head_pin, initial_angle=-90)
        self.beak_shut = -90
        self.sounds = sound_module
        logger.info("crow created")

    # rotate_direction either `right` or not (left)
    # The servo (appears to) struggle to reach 90 (and is noisy in
    # the attempt, so cap at 80 rotation)
    def rotate_caw_times(self, rotate_direction, times):
        logger.info(f"rotate_direction: {rotate_direction}, times: {times}")
        if rotate_direction == 'right':
            angle = -80
        else:
            angle = 80
        self.slow_rotate_to(self.HEAD_SERVO, angle)
        self.caw_x_times(times)
        self.slow_rotate_to(self.HEAD_SERVO, 0)

    # say 'surprise!' one time
    def surprise(self, rotate_direction='left'):
        if rotate_direction == 'right':
            angle = -80
        else:
            angle = 80
        self.slow_rotate_to(self.HEAD_SERVO, angle)
        self.open_mouth_for_sound(self.BEAK_SERVO, audio.SURPRISE_L, 2.0, -90, open_position=30)
        self.slow_rotate_to(self.HEAD_SERVO, 0)

    # Open beak and rotate one direction (L or R), then crow
    # rotation a little slow

    def rotate_and_crow(self):
        self.slow_rotate_to(self.HEAD_SERVO, -90)
        self.caw_caw_caw()
        self.slow_rotate_to(self.HEAD_SERVO, 0)

    def caw_caw_caw(self):
        self.open_mouth_for_sound(self.BEAK_SERVO, audio.CAW_4, 2.5)

    # Given a sound x seconds long, have the servo fully rotated (to its
    # open_position) at time = x/2, and back at shut_position at time = x
    def open_mouth_for_sound(self, servo, sound, time_s, shut_position=-90, open_position=30):
        start_time = time.time()
        self.slow_rotate_to(servo, open_position,
                            interval=0.0001, speed_multiplier=5)
        logger.info(f"playing sound {sound}")
        audio.play(sound)
        elapsed_time = time.time() - start_time
        # count two rotation times, and only sleep for the remaining time in time_s
        time.sleep(time_s - elapsed_time * 2)
        self.slow_rotate_to(servo, shut_position,
                            interval=0.0001, speed_multiplier=5)

    # Open mouth a bit, rotate head, and stare without sound.
    # Crows seem to do this sometimes.

    def open_beak_rotate(self):
        self.open_beak(self.BEAK_SERVO, max_open=30)
        self.slow_oscillate(self.HEAD_SERVO)
        self.open_beak(self.BEAK_SERVO, max_open=-80)

    # for example, with sleep time of 0.1 between each angle-set, the total
    # time comes to 9.66 (so almost all the time is sleep: 90*0.1)
    # a 0.01s sleep time gives a 90-degree rotation in 1.6 seconds
    def slow_oscillate(self, servo, interval=0.01):
        self.slow_rotate_to(servo, 0)
        for angle in range(0, 90):
            servo.angle = angle
            time.sleep(interval)
        for angle in range(90, -90, -1):
            servo.angle = angle
            time.sleep(interval)
        for angle in range(-90, 0):
            servo.angle = angle
            time.sleep(interval)

    # In cases where the current servo position is not what is desired,
    # slowly rotate to that position (to prevent violent jerk to the
    # starting position in some other method)
    def slow_rotate_to(self, servo, target_angle, interval=0.005, speed_multiplier=1):
        initial_angle = int(servo.angle)
        if target_angle > initial_angle:
            step = 1 * speed_multiplier
        else:
            step = -1 * speed_multiplier
        for angle in range(initial_angle, target_angle, step):
            servo.angle = angle

    # max_open takes a value from -90 (beak shut) => +90)
    # The beak appears fully open at +30
    def open_beak(self, servo, max_open):
        initial_angle = -90
        interval = 0.03
        for ang in range(initial_angle, max_open):
            servo.angle = ang
            time.sleep(interval)

    # Caw the given integer times
    def caw_x_times(self, times):
        # iterate through once fewer than `times`
        shut_position = -90
        for x in range(1, times):
            shut_position = 20
            self.open_mouth_for_sound(
                self.BEAK_SERVO, self.sounds.CAW_1, 1.0, shut_position, open_position=30)
        # last iteration shut all the way
        self.open_mouth_for_sound(
            self.BEAK_SERVO, self.sounds.CAW_1, 1.0, shut_position=-90, open_position=30)
