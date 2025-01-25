# File: GameLib\settings.py
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

        # Sound slider
        self.slider_x = 300
        self.slider_y = 200
        self.slider_width = 200
        self.slider_height = 10
        self.slider_knob_x = self.slider_x + 100  # Default position of knob
        self.slider_knob_radius = 10
        self.sound_volume = 0.5  # Default volume (0.0 to 1.0)

        # Difficulty setting
        self.settings = {
            "Difficulty": "Normal",  # Easy, Normal, Hard
        }
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.current_difficulty_index = self.difficulty_levels.index(
            self.settings["Difficulty"]
        )

        # Button for cycling difficulty
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
                        return "main_menu"

                    if self.difficulty_button.isClicked((mx, my)):
                        self.current_difficulty_index = (
                            self.current_difficulty_index + 1
                        ) % len(self.difficulty_levels)
                        self.settings["Difficulty"] = self.difficulty_levels[
                            self.current_difficulty_index
                        ]

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and self.is_mouse_over_slider(mx, my):
                    # Update the knob position and sound volume
                    self.slider_knob_x = max(
                        self.slider_x,
                        min(mx, self.slider_x + self.slider_width),
                    )
                    self.sound_volume = (
                        self.slider_knob_x - self.slider_x
                    ) / self.slider_width
                    print(f"Sound Volume: {self.sound_volume:.2f}")

    def is_mouse_over_slider(self, mx, my):
        """Check if the mouse is over the slider knob."""
        return (
            self.slider_x <= mx <= self.slider_x + self.slider_width
            and self.slider_y - self.slider_knob_radius
            <= my
            <= self.slider_y + self.slider_knob_radius
        )

    def draw_settings_menu(self):
        self.screen.fill((30, 30, 30))

        # Draw buttons
        self.back_button.draw(self.screen)
        self.difficulty_button.draw(self.screen)

        # Draw slider
        pg.draw.rect(
            self.screen,
            (200, 200, 200),
            (self.slider_x, self.slider_y, self.slider_width, self.slider_height),
        )
        pg.draw.circle(
            self.screen,
            (255, 255, 255),
            (self.slider_knob_x, self.slider_y + self.slider_height // 2),
            self.slider_knob_radius,
        )

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
            f"Sound Volume: {int(self.sound_volume * 100)}%",
            self.font,
            (255, 255, 255),
            self.screen,
            self.slider_x,
            self.slider_y - 30,
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
