import arcade
import random
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, BULLET_SPEED
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


class FinalBoss(Enemy):
    def __init__(self):
        super().__init__()
        # Cargar una imagen diferente y más grande para el jefe
        self.texture = arcade.load_texture(":resources:images/space_shooter/playerShip3_orange.png")
        self.scale = 1.5  # Ajustar el tamaño del jefe final
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 100
        self.health = 100  # Vida del jefe final
        self.change_x = 2  # Ajusta el movimiento horizontal
        self.change_y = 0

    def update(self):
        # Movimiento en zig-zag del jefe
        self.center_x += self.change_x
        if self.center_x < 50 or self.center_x > SCREEN_WIDTH - 50:
            self.change_x *= -1

    def take_damage(self, damage):
        """Reducir la vida del jefe cuando recibe daño"""
        self.health -= damage
        if self.health < 0:
            self.health = 0


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.boss = None
        self.game_over = False
        self.win_time = None  # Tiempo de la victoria
        self.boss_health = 100  # Salud del jefe

    def start_final_level(self):
        # Inicia el nivel final y crea el jefe final
        self.boss = FinalBoss()

    def update(self, delta_time):
        if self.boss and not self.game_over:
            self.boss.update()

            # Comprobar si el jefe ha sido derrotado
            if self.boss.health <= 0:
                # Mostramos el texto de "You Win" y terminamos el juego solo cuando la salud es 0
                self.boss = None  # Eliminar jefe cuando su vida es 0
                self.game_over = True  # Marcar el juego como finalizado
                self.win_time = time.time()  # Marca el tiempo de victoria

        if self.game_over:
            if time.time() - self.win_time > 5:
                # Después de 5 segundos, puedes cerrar el juego
                arcade.exit()

    def on_draw(self):
        arcade.start_render()

        if self.boss and self.boss.health > 0:
            self.boss.draw()

        if self.game_over:
            arcade.draw_text("You Win! Gracias por jugar TyrianNavi", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                            arcade.color.WHITE, 54, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.boss:
            self.boss.take_damage(10)  

