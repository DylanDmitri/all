from pygame import mixer
import os


class load_from:
    def __init__(self, directory):
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            name = filename.split('.')[0]

            setattr(self, name, mixer.Sound(path))

sounds = load_from('drum_fun')
