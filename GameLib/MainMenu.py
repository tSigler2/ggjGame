import pygame as pg
import subprocess
import os
from SettingsMenu import SettingsMenu


class MainMenu:
    """
    The MainMenu class handles the main menu of the game, including buttons and navigation.
    """

    def __init__(self, game, screen_width: int, screen_height: int, clock):
        """
        Initialize the main menu.

        Args:
            game: The main game object.
            screen_width: Width of the screen.
            screen_height: Height of the screen.
            clock: Pygame clock object for managing frame rate.
        """
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = clock  # Use the clock passed from Main
        self.font = pg.font.SysFont("Consolas", 20)  # Smaller font for pixelated feel
        self.buttons = self.create_buttons()

    def create_buttons(self) -> list:
        """
        Create buttons for the main menu.

        Returns:
            A list of button dictionaries, each containing a rect and text.
        """
        button_width = 100  # Smaller buttons for pixelated feel
        button_height = 30
        button_spacing = 10

        buttons = [
            {
                "rect": pg.Rect(
                    (self.screen_width - button_width) // 2,
                    (self.screen_height - button_height * 3 - button_spacing * 2) // 2,
                    button_width,
                    button_height,
                ),
                "text": "Start Game",
                "action": self.start_game,
            },
            {
                "rect": pg.Rect(
                    (self.screen_width - button_width) // 2,
                    (self.screen_height - button_height) // 2,
                    button_width,
                    button_height,
                ),
                "text": "Settings",
                "action": self.open_settings,
            },
            {
                "rect": pg.Rect(
                    (self.screen_width - button_width) // 2,
                    (self.screen_height + button_height + button_spacing * 2) // 2,
                    button_width,
                    button_height,
                ),
                "text": "Quit",
                "action": self.quit_game,
            },
        ]
        return buttons

    def start_game(self):
        """
        Start the game by launching Game.py.
        """
        self.game.current_menu = "game"
        self.game.game.init()

    def open_settings(self):
        """
        Open the settings menu by launching Settings.py.
        """
        self.game.current_menu = "settings"

    def quit_game(self):
        """
        Quit the game.
        """
        self.game.running = False

    def handle_events(self):
        """
        Handle user input events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_click(event.pos)

    def handle_click(self, mouse_pos: tuple):
        """
        Handle a mouse click event.

        Args:
            mouse_pos: Position of the mouse click (x, y).
        """
        # Scale the mouse position to the internal resolution
        scaled_mouse_pos = (
            mouse_pos[0] // self.game.scale_factor,
            mouse_pos[1] // self.game.scale_factor,
        )

        for button in self.buttons:
            if button["rect"].collidepoint(scaled_mouse_pos):
                button["action"]()

    def draw(self, surface):
        """
        Draw the main menu, including buttons and text.

        Args:
            surface: The surface to draw on (internal surface).
        """
        surface.fill((30, 30, 30))  # Dark gray background

        # Draw buttons
        for button in self.buttons:
            pg.draw.rect(surface, (0, 0, 255), button["rect"])  # Blue button
            text_surface = self.font.render(
                button["text"], True, (255, 255, 255)
            )  # White text
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)

    def run(self):
        """
        Run the main menu loop.
        """
        while self.game.running and self.game.current_menu == "main":
            self.handle_events()
            self.draw(self.game.internal_surface)
            self.clock.tick(self.game.fps)  # Use the clock passed from Main
