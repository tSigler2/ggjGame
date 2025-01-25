import pygame as pg
import sys
from GameLib.level1 import Level1
from GameLib.test import Test
from GameLib.Menu.Button import Button


class Settings:
    def __init__(
        self, dims, enable_test_level=True
    ):  # init menu with given dimensions and optional test level
        pg.init()  # initialize pygame
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)  # set window size
        pg.display.set_caption("Settings Menu")  # set window title
        self.clock = pg.time.Clock()  # set clock to control framerate
        self.fps = 60  # target frames per second

        # Menu settings
        self.font = pg.font.SysFont("Consolas", 25)
        self.settings = ["Level 1", "Level 2", "Level 3", "Exit"]  # menu items
        self.current_option = 0  # current selected option index

        # Test level button (controlled by enable_test_level)
        self.test_button_text = "Test Level"
        self.test_button_font = pg.font.Font(None, 40)  # font for test button text
        self.test_button_width = 150  # button width
        self.test_button_height = 50  # button height
        self.enable_test_level = (
            enable_test_level  # flag to enable or disable the test level button
        )

        self.start_button = Button(150, 400, 150, 50)
        self.settings_button = Button(350, 400, 150, 50)
        self.quit_button = Button(550, 400, 150, 50)
        self.test_button = Button(350, 200, 150, 50)

    def handle_input(self):
        mx, my = pg.mouse.get_pos()

        for event in pg.event.get():  # loop through events
            if event.type == pg.QUIT:  # quit gamem
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.quit_button.isClicked((mx, my)):
                    pg.quit()
                    sys.exit()

                if event.button == 1 and self.start_button.isClicked((mx, my)):
                    Level1((800, 600)).run()

                if event.button == 1 and self.test_button.isClicked((mx, my)):
                    Test((800, 600)).run()

            # check for mouse click on the test level button if enabled
            if (
                event.type == pg.MOUSEBUTTONDOWN and self.enable_test_level
            ):  # only check if enabled
                mouse_pos = pg.mouse.get_pos()  # get mouse position
                if self.test_button_rect.collidepoint(
                    mouse_pos
                ):  # check if click is inside button
                    self.test_level()  # run test level function

        # handle key and mouse input
        # if self.start_button.isClicked((mx, my)):
        # Level1.run()

    def test_level(self):
        # test level logic (stub for now)
        print("Testing Level")

    def draw_menu(self):
        self.screen.fill((0, 0, 0))  # set background color to black

        self.start_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.test_button.draw(self.screen)

        self.draw_text(
            "Bubble Blast Deluxe Unlimited Edition ft. Glasscord Team",
            self.font,
            (255, 255, 255),
            self.screen,
            int(self.width / 2) - 393,
            20,
        )
        self.draw_text("Start Game", self.font, (255, 255, 255), self.screen, 155, 415)
        self.draw_text("Settings", self.font, (255, 255, 255), self.screen, 375, 415)
        self.draw_text("Test", self.font, (255, 255, 255), self.screen, 395, 215)
        self.draw_text("Quit", self.font, (255, 255, 255), self.screen, 595, 415)

        pg.display.flip()  # update the screen

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def run(self):
        while True:
            self.handle_input()  # handle user input
            self.draw_menu()  # draw the menu
            self.clock.tick(self.fps)  # control framerate
