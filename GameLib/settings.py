import pygame as pg
import sys
from GameLib.Menu.Button import Button


class SettingsMenu:
    def __init__(self, dims):
        pg.init()
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Settings")
        self.clock = pg.time.Clock()
        self.fps = 60

        # Menu settings
        self.font = pg.font.SysFont("Consolas", 25)

        # Buttons
        self.back_button = Button(350, 500, 150, 50)

        # Settings options (examples: toggle and sliders)
        self.settings = {
            "Sound": True,  # True = On, False = Off
            "Difficulty": "Normal",  # Easy, Normal, Hard
        }
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.current_difficulty_index = self.difficulty_levels.index(
            self.settings["Difficulty"]
        )

        # Button rectangles for toggle and cycling settings
        self.sound_toggle_button = Button(350, 200, 150, 50)
        self.difficulty_button = Button(350, 300, 150, 50)

    def handle_input(self):
        mx, my = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.isClicked((mx, my)):
                        return "main_menu"  # Signal to return to main menu

                    if self.sound_toggle_button.isClicked((mx, my)):
                        self.settings["Sound"] = not self.settings["Sound"]

                    if self.difficulty_button.isClicked((mx, my)):
                        self.current_difficulty_index = (
                            self.current_difficulty_index + 1
                        ) % len(self.difficulty_levels)
                        self.settings["Difficulty"] = self.difficulty_levels[
                            self.current_difficulty_index
                        ]

    def draw_settings_menu(self):
        self.screen.fill((30, 30, 30))

        # Draw buttons
        self.back_button.draw(self.screen)
        self.sound_toggle_button.draw(self.screen)
        self.difficulty_button.draw(self.screen)

        # Draw text
        self.draw_text(
            "Settings",
            self.font,
            (255, 255, 255),
            self.screen,
            self.width // 2 - 50,
            50,
        )
        self.draw_text(
            f"Sound: {'On' if self.settings['Sound'] else 'Off'}",
            self.font,
            (255, 255, 255),
            self.screen,
            365,
            215,
        )
        self.draw_text(
            f"Difficulty: {self.settings['Difficulty']}",
            self.font,
            (255, 255, 255),
            self.screen,
            360,
            315,
        )
        self.draw_text("Back", self.font, (255, 255, 255), self.screen, 390, 515)

        pg.display.flip()

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def run(self):
        while True:
            action = self.handle_input()
            if action == "main_menu":
                break
            self.draw_settings_menu()
            self.clock.tick(self.fps)
