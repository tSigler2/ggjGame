from collections import deque
import os
from AnimatedSprite import AnimatedSprite


class MultiAnimatedSprite(AnimatedSprite):
    """
    The MultiAnimatedSprite class handles multiple animation sets.
    """

    def __init__(
        self,
        game,
        path: str,
        pos: tuple,
        scale: float,
        animation_time: int,
        *animation_sets
    ):
        """
        Initialize the multi-animated sprite.

        Args:
            game: The main game object.
            path: Base path to the folder containing animation sets.
            pos: Initial position (x, y) of the sprite.
            scale: Scale factor for the sprite.
            animation_time: Time between animation frames (in milliseconds).
            *animation_sets: Names of animation sets (e.g., "walk", "attack").
        """
        super().__init__(
            game, os.path.join(path, animation_sets[0]), pos, scale, animation_time
        )
        self.animation_sets = {
            name: self.load_animation_frames(os.path.join(path, name))
            for name in animation_sets
        }
        self.current_animation = animation_sets[0]  # Default animation

    def switch_animation(self, animation_name: str):
        """
        Switch to a different animation set.

        Args:
            animation_name: Name of the animation set to switch to.
        """
        if animation_name in self.animation_sets:
            self.current_animation = animation_name
            self.animation_frames = self.animation_sets[animation_name]
            self.current_frame = 0  # Reset to the first frame of the new animation
