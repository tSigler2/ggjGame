from MainMenu import MainMenu
import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")


# Create the game object (dummy for this example)
class Game:

    def __init__(self):
        # Initialize pygame and other necessary game components
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize settings (could be a dictionary or a custom class)
        self.settings = {
            "volume": 100,
            "resolution": (screen_width, screen_height),
            # Add other settings you may need here
        }

    def start_game(self):
        print("Starting the game...")
        
game = Game()

# Create and run the main menu
main_menu = MainMenu(game, screen_width, screen_height, game.clock)
main_menu.run()

# Quit Pygame
pygame.quit()
