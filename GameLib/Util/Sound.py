import pygame as pg


class SoundManager:
    def __init__(self, path, *sounds):
        pg.mixer.init()
        self.path = path
        self.sound_list = {}
        self.music_list = {}

        # sound list initialization seemed incorrect
        self.sound_list = {
            sound[:-4]: pg.mixer.Sound(self.path + sound) for sound in sounds
        }

    def add_sound(self, sound):
        self.sound_list[sound[:-4]] = pg.mixer.Sound(self.path + sound)

    def load_music(self, *music):
        for mu in music:
            self.music_list[mu[:-4]] = mu

    def play_sound(self, sound):
        self.sound_list[sound].play()

    def play_music(self, music):
        pg.mixer.music.unload()
        # changed ph to pg
        pg.mixer.music.load(self.path + self.music_list[music])
        pg.mixer.music.play(-1)

    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def rewind(self):
        pg.mixer.music.rewind()
