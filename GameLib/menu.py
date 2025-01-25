import pygame as pg
import sys
from GameLib.level1 import Level1
from GameLib.level2 import Level2
from GameLib.level3 import Level3
from GameLib.Menu.Button import Button

class Menu:
    def __init__(
        self, dims, enable_test_level=True
    ):  # init menu with given dimensions and optional test level
        pg.init()  # initialize pygame
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)  # set window size
        pg.display.set_caption("Main Menu")  # set window title
        self.clock = pg.time.Clock()  # set clock to control framerate
        self.fps = 60  # target frames per second
        self.click = False #Checks to see if a click was performed

        # Menu options
        self.font = pg.font.SysFont("Consolas", 25)
        self.options = ["Level 1", "Level 2", "Level 3", "Exit"]  # menu items
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
        self.options_button = Button(350, 400, 150, 50)
        self.quit_button = Button(550, 400, 150, 50)


    def handle_input(self):
    
        mx, my = pg.mouse.get_pos()

        # handle key and mouse input
        if self.start_button.isClicked((mx, my), self.click):
            Level1.run()
        
        if self.quit_button.isClicked((mx, my), self.click):
            pg.quit()
            sys.exit()

        for event in pg.event.get():  # loop through events
            if event.type == pg.QUIT:  # quit gamemm
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            # check for mouse click on the test level button if enabled
            if (
                event.type == pg.MOUSEBUTTONDOWN and self.enable_test_level
            ):  # only check if enabled
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

        self.start_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)


        self.draw_text('Glasscord GGJ Game 2025', self.font, (255, 255, 255), self.screen, int(self.width  / 2) - 160, 20)
        self.draw_text('Start Game', self.font, (255, 255, 255), self.screen, 155, 415)
        self.draw_text('Options', self.font, (255, 255, 255), self.screen, 375, 415)
        self.draw_text('Quit', self.font, (255, 255, 255), self.screen, 595, 415)

        pg.display.flip()  # update the screen

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_obj, text_rect)

    def run(self):
        while True:
            self.handle_input()  # handle user input
            self.draw_menu()  # draw the menu
            self.clock.tick(self.fps)  # control framerate
