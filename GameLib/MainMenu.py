# File: GameLib\Menu.py
import pygame as pg
import sys
from GameLib.Settings import UI
from GameLib.Level1 import Level1
from GameLib.Game import Game
from GameLib.Test import Test
from Menu.Button import Button
from GameLib.Settings import *


class Menu:
    def __init__(self, dims, enable_test_level=True):
        pg.init()
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Main Menu")
        self.clock = pg.time.Clock()
        self.fps = 60
        UI.init(self)
        self.font = pg.font.Font(None, 36)  # Default font with size 36

        # Button dimensions and spacing
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 30  # Spacing between buttons

        # Calculate button positions dynamically
        total_height = (
            self.button_height * 3 + self.button_spacing * 2
        )  # Three buttons, two gaps
        start_y = (self.height - total_height) // 2

        self.start_button = Button(
            (self.width - self.button_width) // 2,
            start_y,
            self.button_width,
            self.button_height,
        )
        self.settings_button = Button(
            (self.width - self.button_width) // 2,
            start_y + self.button_height + self.button_spacing,
            self.button_width,
            self.button_height,
        )
        self.quit_button = Button(
            (self.width - self.button_width) // 2,
            start_y + (self.button_height + self.button_spacing) * 2,
            self.button_width,
            self.button_height,
        )

        # Test button (optional)
        self.enable_test_level = enable_test_level
        if self.enable_test_level:
            self.test_button = Button(
                (self.width - self.button_width) // 2,
                start_y - self.button_height - self.button_spacing,
                self.button_width,
                self.button_height,
            )

    def handle_input(self):
        mx, my = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.quit_button.isClicked((mx, my)):
                        pg.quit()
                        sys.exit()

                    if self.start_button.isClicked((mx, my)):
                        Game((1280, 720)).run()

                    if self.settings_button.isClicked((mx, my)):
                        # Open SettingsMenu
                        settings_menu = SettingsMenu((800, 600))
                        settings_menu.run()

                    if self.enable_test_level and self.test_button.isClicked((mx, my)):
                        Test((800, 600)).run()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))

        # Draw title
        title_text = "Bubble Blast Deluxe Unlimited Edition ft. Glasscord Team"
        self.draw_centered_text(
            title_text, self.font, (255, 255, 255), self.width // 2, 50
        )

        # Draw buttons
        self.start_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        if self.enable_test_level:
            self.test_button.draw(self.screen)

        # Draw button text
        self.draw_centered_text(
            "Start Game",
            self.font,
            (255, 255, 255),
            self.width // 2,
            self.start_button.rect.y + 10,
        )
        self.draw_centered_text(
            "Settings",
            self.font,
            (255, 255, 255),
            self.width // 2,
            self.settings_button.rect.y + 10,
        )
        self.draw_centered_text(
            "Quit",
            self.font,
            (255, 255, 255),
            self.width // 2,
            self.quit_button.rect.y + 10,
        )

        if self.enable_test_level:
            self.draw_centered_text(
                "Test",
                self.font,
                (255, 255, 255),
                self.width // 2,
                self.test_button.rect.y + 10,
            )

        pg.display.flip()

    def draw_centered_text(self, text, font, color, center_x, center_y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect(center=(center_x, center_y))
        self.screen.blit(text_obj, text_rect)

    def run(self):
        while True:
            self.handle_input()
            self.draw_menu()
            self.clock.tick(self.fps)
