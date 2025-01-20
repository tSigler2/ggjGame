from Game import Game
from Sprite.Sprite import SpriteObj

class ExSprite(SpriteObj):
    def __init__(self, game, path, pos, scale, shift, velocity):
        super().__init__(game, path, pos, scale, shift)
        self.dx, self.dy = velocity

    def update(self):
        if self.x <= 0 or (self.x + self.IMAGE_HEIGHT) >= self.game.width:
            self.dx *= -1
        if self.y <= 0 or (self.y + self.IMAGE_HEIGHT) >= self.game.height:
            self.dy *=-1

        self.x += self.dx * self.game.delta_time
        self.y += self.dy * self.game.fps
        super().get_sprite()

class GameType(Game):
    def __init__(self, dims, fps=60):
        super().__init__(dims, fps)
        self.obj = ExSprite(self, 'ball.png', (320, 240), 1, 0, (0.3, 0.1))

    def update(self):
        self.screen.fill('black')
        self.obj.update()
        super().update()

if __name__ == '__main__':
    game = GameType((640, 480))
    game.run()
