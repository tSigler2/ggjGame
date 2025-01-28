# Re-work this later
# File: GameLib\SettingsMenu.py
import pygame as pg
import sys


class SettingsMenu:
    """
    The SettingsMenu class handles rendering and interaction with the settings menu.
    """

    def __init__(self, screen, clock, settings):
        """
        Initialize the SettingsMenu.

        Args:
            screen: The Pygame screen object for rendering.
            clock: The Pygame clock object to control the frame rate.
            settings: A dictionary or object storing game settings (e.g., volume, difficulty).
        """
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.width, self.height = screen.get_size()
        self.font = pg.font.Font(None, 36)
        self.running = False
        self.options = [
            {
                "name": "Volume",
                "type": "slider",
                "min": 0,
                "max": 1,
                "step": 0.1,
                "value": settings.get("volume", 0.5),
            },
            {
                "name": "Difficulty",
                "type": "dropdown",
                "options": ["Easy", "Normal", "Hard"],
                "value": settings.get("difficulty", "Normal"),
            },
            {"name": "Back", "type": "button"},
        ]
        self.active_option = 0

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """
        Draw text on the screen.

        Args:
            text: The string to display.
            x: X-coordinate of the text.
            y: Y-coordinate of the text.
            color: The color of the text.
        """
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def draw_menu(self):
        """
        Draw the settings menu.
        """
        self.screen.fill((0, 0, 0))
        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, ((self.width - title.get_width()) // 2, 50))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.active_option else (150, 150, 150)
            if option["type"] == "slider":
                slider_x = 300
                slider_width = 200
                slider_value_x = (
                    slider_x
                    + (option["value"] - option["min"])
                    / (option["max"] - option["min"])
                    * slider_width
                )
                self.draw_text(
                    f"{option['name']}: {option['value']:.1f}", 100, 150 + i * 60, color
                )
                pg.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (slider_x, 150 + i * 60 + 15, slider_width, 5),
                )
                pg.draw.circle(
                    self.screen, color, (int(slider_value_x), 150 + i * 60 + 18), 10
                )

            elif option["type"] == "dropdown":
                self.draw_text(
                    f"{option['name']}: {option['value']}", 100, 150 + i * 60, color
                )

            elif option["type"] == "button":
                self.draw_text(option["name"], 100, 150 + i * 60, color)

    def handle_input(self):
        """
        Handle user input for navigating and interacting with the settings menu.
        """
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.active_option = (self.active_option - 1) % len(self.options)
                elif event.key == pg.K_DOWN:
                    self.active_option = (self.active_option + 1) % len(self.options)
                elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.select_option()
                elif (
                    event.key == pg.K_LEFT
                    and self.options[self.active_option]["type"] == "slider"
                ):
                    self.adjust_slider(-1)
                elif (
                    event.key == pg.K_RIGHT
                    and self.options[self.active_option]["type"] == "slider"
                ):
                    self.adjust_slider(1)

    def adjust_slider(self, direction):
        """
        Adjust the value of the currently selected slider option.

        Args:
            direction: -1 to decrease, 1 to increase.
        """
        option = self.options[self.active_option]
        if option["type"] == "slider":
            step = option["step"]
            option["value"] = max(
                option["min"], min(option["max"], option["value"] + direction * step)
            )
            self.settings["volume"] = option["value"]

    def select_option(self):
        """
        Handle the selection of the currently active menu option.
        """
        option = self.options[self.active_option]
        if option["type"] == "dropdown":
            current_index = option["options"].index(option["value"])
            option["value"] = option["options"][
                (current_index + 1) % len(option["options"])
            ]
            self.settings["difficulty"] = option["value"]
        elif option["type"] == "button" and option["name"] == "Back":
            self.running = False

    def run(self):
        """
        Run the settings menu loop.
        """
        self.running = True
        while self.running:
            self.handle_input()
            self.draw_menu()
            pg.display.flip()
            self.clock.tick(30)
