# Enable headphone audio out via raspi-config

# An alternate way of determining the correct mouth movements could be a volume sensor; ie if it's not possible to determine loudness _before_ a sound is made.
from logger import logger

from pygame import mixer

# volume range from 0 to 1
mixer.init()
mixer.music.set_volume(1)

# play sound
def play(filename):
    logger.info(f"play {filename}")
    full_path = SOUND_FILE_ROOT + filename
    mixer.music.load(full_path)
    logger.info(f"mixer {mixer.music}")
    mixer.music.play()


SOUND_FILE_ROOT = '/home/pi/crow_friend/sounds/'

# woow_x - 1.7913730144500732
WOOW_X = 'woow_x.wav'

CROW_4 = 'crow_4.wav'
# surprise motherfucker!
SURPRISE = 'surprise.mp3'
SURPRISE_L = 'surprise_louder.mp3'
# 1 Caw, 700ms
CAW_1  = 'crow_1_loud.mp3'
# 4 caws, 3s
CAW_4 = 'crow_4.wav'
# 1 Caw, 700ms
CROW_1  = 'crow_1.mp3'
