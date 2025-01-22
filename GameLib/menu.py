import pygame as pg
import sys
from level1 import Level1
from level2 import Level2
from level3 import Level3


class Menu:
    def __init__(self, dims):
        # Initialize PyGame and menu variables
        pg.init()
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Main Menu")
        self.clock = pg.time.Clock()
        self.fps = 60

        # Menu options
        self.font = pg.font.Font(None, 50)  # Default font
        self.options = ["Level 1", "Level 2","Level 3", "Exit"]
        self.current_option = 0

    def handle_input(self):
        # Navigate the menu
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.current_option = (self.current_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:
                    self.current_option = (self.current_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN:
                    # Handle menu selection
                    if self.current_option == 0:
                        Level1((800, 600)).run()  # Start Level 1
                    elif self.current_option == 1:
                        Level2((800, 600)).run()  # Start Level 2
                    elif self.current_option == 2:
                        Level2((800, 600)).run()  # Start Level 3
                    elif self.current_option == 3:
                        pg.quit()
                        sys.exit()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw menu options
        for i, option in enumerate(self.options):
            color = (
                (255, 255, 0) if i == self.current_option else (255, 255, 255)
            )  # Highlight current option
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 100))
            self.screen.blit(text, text_rect)

        pg.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.draw_menu()
            self.clock.tick(self.fps)
