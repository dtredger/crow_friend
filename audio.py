# Enable headphone audio out via raspi-config

import pygame

# An alternate way of determining the correct mouth movements could be a volume sensor; ie if it's not possible to determine loudness _before_ a sound is made.

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
