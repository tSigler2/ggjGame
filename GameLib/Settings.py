# File: GameLib\Settings.py
import pygame as pg
import sys
from GameLib.Menu.Button import Button


class EventHandler:
    @staticmethod
    def run():
        EventHandler.events = pg.event.get()

    @staticmethod
    def clicked() -> bool:
        return any(e.type == pg.MOUSEBUTTONDOWN for e in EventHandler.events)


UNSELECTED = "red"
SELECTED = "white"
BUTTONSTATES = {True: SELECTED, False: UNSELECTED}


class UI:
    @staticmethod
    def init(app):
        UI.font = pg.font.SysFont("Consolas", 25)
        UI.sfont = pg.font.SysFont("Consolas", 20)
        UI.lfont = pg.font.SysFont("Consolas", 40)
        UI.xlfont = pg.font.SysFont("Consolas", 50)
        UI.center = (app.screen.get_size()[0] // 2, app.screen.get_size()[1] // 2)
        UI.fonts = {"sm": UI.sfont, "m": UI.font, "l": UI.lfont, "xl": UI.xlfont}


class Slider:
    def __init__(
        self, pos: tuple, size: tuple, initial_val: float, min: int, max: int
    ) -> None:
        self.pos = pos
        self.size = size
        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)
        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

        self.container_rect = pg.Rect(
            self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1]
        )
        self.button_rect = pg.Rect(
            self.slider_left_pos + self.initial_val - 5,
            self.slider_top_pos,
            10,
            self.size[1],
        )

        self.text = UI.fonts["m"].render(
            str(int(self.get_value())), True, "white", None
        )
        self.label_rect = self.text.get_rect(
            center=(self.pos[0], self.slider_top_pos - 15)
        )

        self.grabbed = False

    def move_slider(self, mouse_pos):
        if self.grabbed:
            pos = mouse_pos[0]
            pos = max(self.slider_left_pos, min(pos, self.slider_right_pos))
            self.button_rect.centerx = pos
            pg.mixer.music.set_volume(self.get_value() / 100)

    def render(self, app):
        pg.draw.rect(app.screen, "darkgray", self.container_rect)
        pg.draw.rect(app.screen, BUTTONSTATES[self.hovered()], self.button_rect)

    def hovered(self):
        return self.container_rect.collidepoint(pg.mouse.get_pos())

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self, app):
        self.text = UI.fonts["m"].render(
            str(int(self.get_value())), True, "white", None
        )
        app.screen.blit(self.text, self.label_rect)


class SettingsMenu:
    def __init__(self, dims):
        pg.init()
        pg.mixer.init()  # Initialize the mixer module for audio
        self.width, self.height = dims
        self.screen = pg.display.set_mode(dims)
        pg.display.set_caption("Settings")
        self.clock = pg.time.Clock()
        self.fps = 60

        # Menu settings
        self.font = pg.font.SysFont("Consolas", 25)

        # Buttons
        self.back_button = Button(350, 500, 150, 50)

        # Difficulty setting
        self.settings = {
            "Difficulty": "Normal",  # Easy, Normal, Hard
            "Volume": 50,  # Volume slider position, 0 to 100
        }
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.current_difficulty_index = self.difficulty_levels.index(
            self.settings["Difficulty"]
        )

        # Button for cycling difficulty
        self.difficulty_button = Button(350, 300, 150, 50)

        # Create Slider for volume control
        self.volume_slider = Slider(
            (self.width // 2, 400), (200, 30), self.settings["Volume"] / 100, 0, 100
        )

        # Load and play TownTheme.mp3 in a loop
        self.music = pg.mixer.Sound("GameLib/Assets/sounds/TownTheme.mp3")
        self.music.set_volume(
            self.settings["Volume"] / 100.0
        )  # Set initial volume (0.0 to 1.0)
        self.music.play(-1)  # Play the music in a loop

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

                    # Check if volume slider is clicked and update the volume
                    if self.volume_slider.container_rect.collidepoint(mx, my):
                        self.volume_slider.grabbed = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.volume_slider.grabbed = False

            # Move the slider if it's being grabbed
            if self.volume_slider.grabbed:
                self.volume_slider.move_slider((mx, my))
                # Update the settings volume based on the slider value
                self.settings["Volume"] = int(self.volume_slider.get_value())

                # Set the music volume based on the slider value (0 to 1)
                self.music.set_volume(self.volume_slider.get_value() / 100.0)

    def draw_settings_menu(self):
        self.screen.fill((30, 30, 30))

        # Draw buttons
        self.back_button.draw(self.screen)
        self.difficulty_button.draw(self.screen)

        # Draw volume slider
        self.volume_slider.render(self)
        self.volume_slider.display_value(self)

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
            f"Difficulty: {self.settings['Difficulty']}",
            self.font,
            (255, 255, 255),
            self.screen,
            360,
            315,
        )
        self.draw_text(
            f"Volume: {self.settings['Volume']}",
            self.font,
            (255, 255, 255),
            self.screen,
            self.volume_slider.pos[0] - self.volume_slider.size[0] // 2 - 160,
            self.volume_slider.pos[1] - 10,
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
