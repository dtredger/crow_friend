# Enable headphone audio out via raspi-config

import threading

# An alternate way of determining the correct mouth movements could be a volume sensor; ie if it's not possible to determine loudness _before_ a sound is made.

# woow_x - 1.7913730144500732
SOUND_FILE_ROOT = '/home/pi/crow_friend/sounds/'

WOOW_X = 'woow_x.wav'
CROW_4 = 'crow_4.wav'
SURPRISE = 'surprise.mp3'

# 1 Caw, 700ms
CROW_1  = 'crow_1.mp3'

# ****


# https://stackoverflow.com/questions/5179467/equivalent-of-setinterval-in-python
def set_interval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()
            # This is another function to be executed
            # in a different thread to simulate set_interval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1
            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap
