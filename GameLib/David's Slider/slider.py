import pygame
import sys
import os


class EventHandler:
    @staticmethod
    def run():
        EventHandler.events = pygame.event.get()

    @staticmethod
    def clicked() -> bool:
        return any(e.type == pygame.MOUSEBUTTONDOWN for e in EventHandler.events)


UNSELECTED = "red"
SELECTED = "white"
BUTTONSTATES = {True: SELECTED, False: UNSELECTED}


class UI:
    @staticmethod
    def init(app):
        UI.font = pygame.font.Font(None, 30)
        UI.sfont = pygame.font.Font(None, 20)
        UI.lfont = pygame.font.Font(None, 40)
        UI.xlfont = pygame.font.Font(None, 50)
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

        self.container_rect = pygame.Rect(
            self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1]
        )
        self.button_rect = pygame.Rect(
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
            pygame.mixer.music.set_volume(self.get_value() / 100)

    def render(self, app):
        pygame.draw.rect(app.screen, "darkgray", self.container_rect)
        pygame.draw.rect(app.screen, BUTTONSTATES[self.hovered()], self.button_rect)

    def hovered(self):
        return self.container_rect.collidepoint(pygame.mouse.get_pos())

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self, app):
        self.text = UI.fonts["m"].render(
            str(int(self.get_value())), True, "white", None
        )
        app.screen.blit(self.text, self.label_rect)


class Menu:
    def __init__(self, app, bg="gray") -> None:
        self.app = app
        self.bg = bg
        self.sliders = [Slider(UI.center, (100, 30), 0.5, 0, 100)]

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        self.app.screen.fill("black")
        for slider in self.sliders:
            if slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
                slider.grabbed = True
            elif not mouse[0]:
                slider.grabbed = False

            slider.move_slider(mouse_pos)
            slider.render(self.app)
            slider.display_value(self.app)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        UI.init(self)
        self.clock = pygame.time.Clock()

        file = os.path.join(os.path.dirname(__file__), "TownTheme.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        self.menu = Menu(self)

    def run(self):
        self.running = True
        while self.running:
            EventHandler.run()
            for e in EventHandler.events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.menu.run()

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
