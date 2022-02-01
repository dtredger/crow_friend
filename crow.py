# Enable headphone audio out via raspi-config
#
import pygame

# woow_x - 1.7913730144500732
woow_x ='/home/pi/Documents/crow_friend/sounds/woow_x.wav'

sounds = {
    "woow_x": {
        "path": "/home/pi/Documents/crow_friend/sounds/woow_x.wav",
        "duration_s": "1.79"
    }
}

def play(sound_path="/home/pi/radio_pi/left_right.wav"):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()


# ----- ALT method ---
# /usr/lib/python3/dist-packages/gpiozero/output_devices.py:1533: PWMSoftwareFallback: To reduce servo jitter, use the pigpio pin factory.See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo for more info
from gpiozero import Servo
from time import sleep

servo = Servo(25)

# HEAD_SERVO_PIN = 25
# head_servo = Servo(HEAD_SERVO_PIN)
#
#

# servo.all              servo.is_active        servo.min_pulse_width  servo.source_delay
# servo.close(           servo.max(             servo.namedtuple(      servo.value
# servo.closed           servo.max_pulse_width  servo.pin_factory      servo.values
# servo.detach(          servo.mid(             servo.pulse_width
# servo.frame_width      servo.min(             servo.source



# Given a sound x seconds long, have the servo fully rotated (to its
# rotation max r_max) at time = x/2, and back at original time at
# time = x
def open_for_sound(time_s):
    servo.max()
    play(woow_x)
    sleep(time_s/2)
    servo.min()
    sleep(time_s/2)

def rotate_head():
    head_servo


def rotate_and_crow():



# def stop_servos():
#     pwm.stop()
#     GPIO.cleanup()
