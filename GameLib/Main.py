from MainMenu import MainMenu
import pygame as pg

# Initialize Pygame
pg.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Main Menu")


# Create the game object (dummy for this example)
class Game:
    def __init__(self):
        self.screen = screen
        self.running = True

    def start_game(self):
        print("Starting the game...")


game = Game()

# Create and run the main menu
main_menu = MainMenu(game, screen_width, screen_height)
main_menu.run()

# Quit Pygame
pg.quit()
