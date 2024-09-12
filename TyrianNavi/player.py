import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("img/A1.png")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y=50
        self.speed=5

    def update(self):
        super().update()

        # Evitar que se salga de la pantalla
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT