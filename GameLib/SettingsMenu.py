import pygame as pg


class SettingsMenu:
    """
    The SettingsMenu class handles the settings menu, including volume control and difficulty selection.
    """

    def __init__(self, game, screen_width: int, screen_height: int):
        """
        Initialize the settings menu.

        Args:
            game: The main game object.
            screen_width: Width of the screen.
            screen_height: Height of the screen.
        """
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pg.font.SysFont("Consolas", 40)
        self.small_font = pg.font.SysFont("Consolas", 30)
        self.buttons = self.create_buttons()
        self.sliders = self.create_sliders()
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.current_difficulty_index = 1  # Default to "Normal"

    def create_buttons(self) -> list:
        """
        Create buttons for the settings menu.

        Returns:
            A list of button dictionaries, each containing a rect and text.
        """
        button_width = 200
        button_height = 50
        button_spacing = 20

        buttons = [
            {
                "rect": pg.Rect(
                    (self.screen_width - button_width) // 2,
                    self.screen_height - button_height - button_spacing,
                    button_width,
                    button_height,
                ),
                "text": "Back",
                "action": self.go_back,
            },
            {
                "rect": pg.Rect(
                    (self.screen_width - button_width) // 2,
                    (self.screen_height - button_height * 3 - button_spacing * 2) // 2,
                    button_width,
                    button_height,
                ),
                "text": "Difficulty",
                "action": self.change_difficulty,
            },
        ]
        return buttons

    def create_sliders(self) -> list:
        """
        Create sliders for the settings menu.

        Returns:
            A list of slider dictionaries, each containing a rect and value.
        """
        slider_width = 200
        slider_height = 20
        slider_spacing = 50

        sliders = [
            {
                "rect": pg.Rect(
                    (self.screen_width - slider_width) // 2,
                    (self.screen_height - slider_height * 2 - slider_spacing) // 2,
                    slider_width,
                    slider_height,
                ),
                "value": 50,  # Default volume level (0-100)
                "type": "volume",
            },
        ]
        return sliders

    def go_back(self):
        """
        Return to the main menu.
        """
        self.game.current_menu = "main"

    def change_difficulty(self):
        """
        Cycle through difficulty levels.
        """
        self.current_difficulty_index = (self.current_difficulty_index + 1) % len(
            self.difficulty_levels
        )
        print(
            f"Difficulty set to: {self.difficulty_levels[self.current_difficulty_index]}"
        )

    def handle_events(self, event):
        """
        Handle user input events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_click(event.pos)
            elif event.type == pg.MOUSEMOTION:
                self.handle_slider_drag(pg.mouse.get_pos())

    def handle_click(self, mouse_pos: tuple):
        """
        Handle a mouse click event.

        Args:
            mouse_pos: Position of the mouse click (x, y).
        """
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button["action"]()

    def handle_slider_drag(self, mouse_pos: tuple):
        """
        Handle slider dragging.

        Args:
            mouse_pos: Position of the mouse (x, y).
        """
        for slider in self.sliders:
            if slider["rect"].collidepoint(mouse_pos):
                slider["value"] = int(
                    (mouse_pos[0] - slider["rect"].x) / slider["rect"].width * 100
                )
                slider["value"] = max(
                    0, min(100, slider["value"])
                )  # Clamp value between 0 and 100
                if slider["type"] == "volume":
                    self.game.sound_manager.set_volume(slider["value"] / 100)

    def draw(self, surface):
        """
        Draw the settings menu, including buttons, sliders, and text.
        """
        surface.fill((50, 50, 50))  # Dark gray background

        # Draw buttons
        for button in self.buttons:
            pg.draw.rect(self.game.screen, (0, 0, 255), button["rect"])  # Blue button
            text_surface = self.font.render(
                button["text"], True, (255, 255, 255)
            )  # White text
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)

        # Draw sliders
        for slider in self.sliders:
            pg.draw.rect(
                self.game.screen, (100, 100, 100), slider["rect"]
            )  # Gray slider track
            handle_x = slider["rect"].x + int(
                slider["value"] / 100 * slider["rect"].width
            )
            handle_rect = pg.Rect(
                handle_x - 5, slider["rect"].y, 10, slider["rect"].height
            )
            pg.draw.rect(
                self.game.screen, (0, 255, 0), handle_rect
            )  # Green slider handle

        # Draw difficulty text
        difficulty_text = (
            f"Difficulty: {self.difficulty_levels[self.current_difficulty_index]}"
        )
        text_surface = self.small_font.render(difficulty_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 50)
        )
        self.game.screen.blit(text_surface, text_rect)

        pg.display.flip()

    def run(self):
        """
        Run the settings menu loop.
        """
        while self.game.current_menu == "settings":
            self.handle_events()
            self.draw()
