import pygame as pg
from collections import deque
import os
from Sprite import Sprite


class AnimatedSprite(Sprite):
    """
    The AnimatedSprite class handles a single animation sequence.
    """

    def __init__(self, game, path: str, pos: tuple, scale: float, animation_time: int):
        """
        Initialize the animated sprite.

        Args:
            game: The main game object.
            path: Path to the folder containing animation frames.
            pos: Initial position (x, y) of the sprite.
            scale: Scale factor for the sprite.
            animation_time: Time between animation frames (in milliseconds).
        """
        super().__init__(game, os.path.join(path, "frame0.png"), pos, scale)
        self.animation_time = animation_time
        self.animation_frames = self.load_animation_frames(path)
        self.current_frame = 0
        self.last_frame_time = pg.time.get_ticks()

    def load_animation_frames(self, path: str) -> deque:
        """
        Load animation frames from the specified folder.

        Args:
            path: Path to the folder containing animation frames.

        Returns:
            A deque of animation frames.
        """
        frames = deque()
        for file in sorted(os.listdir(path)):
            if file.endswith((".png", ".jpg")):
                img = pg.image.load(os.path.join(path, file)).convert_alpha()
                img = pg.transform.scale(
                    img,
                    (
                        int(img.get_width() * self.scale),
                        int(img.get_height() * self.scale),
                    ),
                )
                frames.append(img)
        return frames

    def update(self):
        """
        Update the animation and draw the sprite.
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time >= self.animation_time:
            self.last_frame_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]

        super().draw()
