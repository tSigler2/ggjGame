import os
import pygame as pg


class SoundManager:
    def __init__(self, path, *sounds):
        pg.mixer.init()
        self.path = path
        # sound list initialization seemed incorrect
        self.sound_list = {
            sound[:-4]: pg.mixer.Sound(os.path.join(path, sound)) for sound in sounds
        }
        self.music_list = {}

    def add_sound(self, sound):
        self.sound_list[sound[:-4]] = pg.mixer.Sound(self.path + sound)

    def load_music(self, *music):
        for mu in music:
            self.music_list[mu[:-4]] = mu

    def play_sound(self, sound):
        self.sound_list[sound].play()

    def play_music(self, music_file):
        pg.mixer.music.load(os.path.join(self.path, music_file))
        pg.mixer.music.play(-1)

    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def rewind(self):
        pg.mixer.music.rewind()
