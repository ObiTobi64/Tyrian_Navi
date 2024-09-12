import random
import arcade
from constants import SCREEN_WIDTH, ENEMY_SPEED, BULLET_SPEED
from bullet import Bullet

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png")
        self.center_x = random.randint(50, SCREEN_WIDTH - 50)
        self.center_y = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH)
        self.change_x = random.choice([-1, 1]) * ENEMY_SPEED

    def update(self):
        super().update()

        # Movimiento del enemigo
        self.center_y -= ENEMY_SPEED
        self.center_x += self.change_x

        # Rebote en los bordes
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.change_x *= -1
        elif self.left < 0:
            self.left = 0
            self.change_x *= -1

    def shoot(self):

        bullet = Bullet(":resources:images/space_shooter/laserRed01.png", self)
        bullet.change_y = -BULLET_SPEED
        return bullet