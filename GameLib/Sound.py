import pygame as pg
import os


class SoundManager:
    """
    The SoundManager class handles sound effects and music for the game.
    """

    def __init__(self, sounds_path: str, music_path: str):
        """
        Initialize the sound manager.

        Args:
            sounds_path: Path to the folder containing sound effects.
            music_path: Path to the folder containing music files.
        """
        pg.mixer.init()
        self.sounds_path = sounds_path
        self.music_path = music_path
        self.sound_effects = {}  # Dictionary to store sound effects
        self.music_tracks = {}  # Dictionary to store music tracks
        self.current_music = None  # Currently playing music track

    def load_sound(self, sound_name: str, file_name: str):
        """
        Load a sound effect into the sound manager.

        Args:
            sound_name: Name to associate with the sound effect.
            file_name: Name of the sound file (e.g., "explosion.wav").
        """
        file_path = os.path.join(self.sounds_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Sound file '{file_path}' not found.")
        self.sound_effects[sound_name] = pg.mixer.Sound(file_path)

    def load_music(self, music_name: str, file_name: str):
        """
        Load a music track into the sound manager.

        Args:
            music_name: Name to associate with the music track.
            file_name: Name of the music file (e.g., "background.mp3").
        """
        file_path = os.path.join(self.music_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Music file '{file_path}' not found.")
        self.music_tracks[music_name] = file_path

    def play_sound(self, sound_name: str, loops: int = 0):
        """
        Play a sound effect.

        Args:
            sound_name: Name of the sound effect to play.
            loops: Number of times to loop the sound (0 for no looping).
        """
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].play(loops=loops)
        else:
            print(f"Warning: Sound '{sound_name}' not found.")

    def play_music(self, music_name: str, loops: int = -1):
        """
        Play a music track.

        Args:
            music_name: Name of the music track to play.
            loops: Number of times to loop the music (-1 for infinite looping).
        """
        if music_name in self.music_tracks:
            pg.mixer.music.load(self.music_tracks[music_name])
            pg.mixer.music.play(loops=loops)
            self.current_music = music_name
        else:
            print(f"Warning: Music track '{music_name}' not found.")

    def stop_music(self):
        """
        Stop the currently playing music track.
        """
        pg.mixer.music.stop()
        self.current_music = None

    def pause_music(self):
        """
        Pause the currently playing music track.
        """
        pg.mixer.music.pause()

    def unpause_music(self):
        """
        Unpause the currently paused music track.
        """
        pg.mixer.music.unpause()

    def set_volume(self, volume: float):
        """
        Set the volume for all sounds and music.

        Args:
            volume: Volume level (0.0 to 1.0).
        """
        pg.mixer.music.set_volume(volume)
        for sound in self.sound_effects.values():
            sound.set_volume(volume)
