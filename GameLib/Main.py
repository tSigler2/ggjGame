import pygame as pg
from MainMenu import MainMenu
from Game import Game
from SettingsMenu import SettingsMenu


class Main:
    """
    The Main class serves as the entry point for the game.
    It initializes Pygame, sets up the game loop, and manages the main menu and game states.
    """

    def __init__(self):
        """
        Initialize the game.
        """
        # Initialize Pygame
        pg.init()

        # Set up the screen
        self.internal_width = 320  # Internal resolution (320x240)
        self.internal_height = 240
        self.scale_factor = 4  # Scale factor for pixelated effect
        self.screen_width = (
            self.internal_width * self.scale_factor
        )  # Window size (1280x960)
        self.screen_height = self.internal_height * self.scale_factor

        # Create the internal surface and the scaled-up window
        self.internal_surface = pg.Surface((self.internal_width, self.internal_height))
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption(
            "Squirrely Pop: The Last Stand"
        )

        # Game state
        self.running = True
        self.current_menu = "main"  # Current menu state ("main", "settings", "game")
        self.clock = pg.time.Clock()
        self.fps = 60

        # Initialize game components
        self.game = Game(self)  # Pass the Main instance to Game
        self.main_menu = MainMenu(
            self, self.internal_width, self.internal_height, self.clock
        )  # Pass clock
        self.settings_menu = SettingsMenu(
            self, self.internal_width, self.internal_height
        )

    def run(self):
        """
        Run the game loop.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        # Quit Pygame
        pg.quit()

    def handle_events(self):
        """
        Handle user input events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            else:
                if self.current_menu == "main":
                    self.main_menu.handle_events(event)  # Pass event
                elif self.current_menu == "settings":
                    self.settings_menu.handle_events(event)
                elif self.current_menu == "game":
                    self.game.handle_events(event)

    def update(self):
        """
        Update the game state based on the current menu.
        """
        if self.current_menu == "main":
            for event in pg.event.get():
                self.main_menu.handle_events(event)
        elif self.current_menu == "settings":
            self.settings_menu.handle_events(event)
        elif self.current_menu == "game":
            self.game.update()

    def draw(self):
        """
        Draw the current menu or game state.
        """
        # Clear the internal surface
        self.internal_surface.fill((0, 0, 0))

        # Draw the current menu or game state to the internal surface
        if self.current_menu == "main":
            self.main_menu.draw(self.internal_surface)
        elif self.current_menu == "settings":
            self.settings_menu.draw(self.internal_surface)
        elif self.current_menu == "game":
            self.game.draw(self.internal_surface)

        # Scale the internal surface to the window size
        scaled_surface = pg.transform.scale(
            self.internal_surface, (self.screen_width, self.screen_height)
        )
        self.screen.blit(scaled_surface, (0, 0))

        pg.display.flip()

    def start_game(self):
        """
        Start the game.
        """
        self.current_menu = "game"
        self.game.init()

    def open_settings(self):
        """
        Open the settings menu.
        """
        self.current_menu = "settings"

    def quit_game(self):
        """
        Quit the game.
        """
        self.running = False


if __name__ == "__main__":
    # Create and run the game
    main = Main()
    main.run()
