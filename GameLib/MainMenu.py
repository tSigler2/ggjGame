import pygame as pg
import subprocess
import os
from Settings import SettingsMenu


class MainMenu:
    """
    The MainMenu class handles the main menu of the game, including buttons and navigation.
    """

    def __init__(self, game, screen_width: int, screen_height: int):
        """
        Initialize the main menu.

        Args:
            game: The main game object.
            screen_width: Width of the screen.
            screen_height: Height of the screen.
        """
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pg.font.SysFont("Consolas", 40)
        self.buttons = self.create_buttons()

    def create_buttons(self) -> list:
        """
        Create buttons for the main menu.

        Returns:
            A list of button dictionaries, each containing a rect and text.
        """
        button_width = 200
        button_height = 50
        button_spacing = 20

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
        game_path = os.path.join(os.path.dirname(__file__), 'Game.py')
        subprocess.Popen(['python', game_path])  # Ensure the correct path is passed
        self.game.running = False  # Stop the main menu

    def open_settings(self):
        """
        Open the settings menu.
        """
        settings_menu = SettingsMenu(self.game, self.screen_width, self.screen_height)
        settings_menu.run()

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
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button["action"]()

    def draw(self):
        """
        Draw the main menu, including buttons and text.
        """
        self.game.screen.fill((30, 30, 30))  # Dark gray background

        # Draw buttons
        for button in self.buttons:
            pg.draw.rect(self.game.screen, (0, 0, 255), button["rect"])  # Blue button
            text_surface = self.font.render(
                button["text"], True, (255, 255, 255)
            )  # White text
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.game.screen.blit(text_surface, text_rect)

        pg.display.flip()

    def run(self):
        """
        Run the main menu loop.
        """
        while self.game.running:
            self.handle_events()
            self.draw()
