import arcade
from constants import BULLET_SPEED, SCREEN_HEIGHT

class Bullet(arcade.Sprite):
    def __init__(self, image, sprite_source):
        super().__init__(image)
        self.center_x =sprite_source.center_x
        self.bottom = sprite_source.top 
        self.change_y = BULLET_SPEED if sprite_source.change_y >= 0 else -BULLET_SPEED

    def update(self):
        super().update()

        # Eliminar la bala si sale de la pantalla
        if self.bottom > SCREEN_HEIGHT or self.top < 0:
            self.remove_from_sprite_lists()