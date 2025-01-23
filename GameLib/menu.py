import pygame as pg
import sys
from GameLib.level1 import Level1
from GameLib.level2 import Level2
from GameLib.level3 import Level3
from GameLib.level4 import Level4
from GameLib.level5 import Level5


class Menu:
    def __init__(self, dims, enable_test_level=True, padding_top=50):
        pg.init()  # initialize pygame
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)  # set window size
        pg.display.set_caption("Main Menu")  # set window title
        self.clock = pg.time.Clock()  # set clock to control framerate
        self.fps = 60  # target frames per second

        # Menu options
        self.font = pg.font.Font(None, 50)  # default font for menu options
        self.options = [
            "Level 1",
            "Level 2",
            "Level 3",
            "Level 4",
            "Level 5",
            "Exit",
        ]  # menu items
        self.current_option = 0  # current selected option index

        # Test level button (controlled by enable_test_level)
        self.test_button_text = "Test Level"
        self.test_button_font = pg.font.Font(None, 40)  # font for test button text
        self.test_button_width = 150  # button width
        self.test_button_height = 50  # button height
        self.enable_test_level = (
            enable_test_level  # flag to enable or disable the test level button
        )
        self.padding_top = padding_top  # padding from top of the screen

    def handle_input(self):
        # handle key and mouse input
        keys = pg.key.get_pressed()  # get all pressed keys

        for event in pg.event.get():  # loop through events
            if event.type == pg.QUIT:  # quit game
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:  # handle key presses
                if event.key == pg.K_UP:  # move up through options
                    self.current_option = (self.current_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:  # move down through options
                    self.current_option = (self.current_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN:  # handle selection
                    if self.current_option == 0:
                        Level1((800, 600)).run()  # start level 1
                    elif self.current_option == 1:
                        Level2((800, 600)).run()  # start level 2
                    elif self.current_option == 2:
                        Level3((800, 600)).run()  # start level 3
                    elif self.current_option == 3:
                        Level4((800, 600)).run()  # start level 4
                    elif self.current_option == 4:
                        Level5((800, 600)).run()  # start level 5
                    elif self.current_option == 5:
                        pg.quit()  # exit game
                        sys.exit()

            # check for mouse click on the test level button if enabled
            if event.type == pg.MOUSEBUTTONDOWN and self.enable_test_level:
                mouse_pos = pg.mouse.get_pos()  # get mouse position
                if self.test_button_rect.collidepoint(
                    mouse_pos
                ):  # check if click is inside button
                    self.test_level()  # run test level function

    def test_level(self):
        # test level logic (stub for now)
        print("Testing Level")

    def draw_menu(self):
        self.screen.fill((0, 0, 0))  # set background color to black

        # Calculate total space for options and adjust positioning
        total_menu_height = len(self.options) * 100  # space between menu options
        total_button_height = (
            self.test_button_height + 20 if self.enable_test_level else 0
        )
        available_space = (
            self.height - total_menu_height - total_button_height - self.padding_top
        )
        start_y = (
            self.padding_top + available_space // 2
        )  # to center the menu vertically with padding

        # draw menu options
        for i, option in enumerate(self.options):
            color = (
                (255, 255, 0) if i == self.current_option else (255, 255, 255)
            )  # highlight current option
            text = self.font.render(option, True, color)  # render text
            text_rect = text.get_rect(
                center=(self.width // 2, start_y + i * 100)
            )  # position text
            self.screen.blit(text, text_rect)  # draw text to screen

        # draw the "Test Level" button if enabled
        if self.enable_test_level:
            self.test_button_rect = pg.Rect(
                self.width - self.test_button_width - 20,
                self.height - self.test_button_height - 20,
                self.test_button_width,
                self.test_button_height,
            )  # set button rectangle
            pg.draw.rect(
                self.screen, (255, 255, 0), self.test_button_rect
            )  # draw button background
            test_button_text = self.test_button_font.render(
                self.test_button_text, True, (0, 0, 0)
            )  # render button text
            test_button_text_rect = test_button_text.get_rect(
                center=self.test_button_rect.center
            )  # position button text
            self.screen.blit(
                test_button_text, test_button_text_rect
            )  # draw button text

        pg.display.flip()  # update the screen

    def run(self):
        while True:
            self.handle_input()  # handle user input
            self.draw_menu()  # draw the menu
            self.clock.tick(self.fps)  # control framerate
