import random
import arcade
from explosion import Explosion
from player import Player
from enemy import Enemy
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, PLAYER_LIVES, SPAWN_RATE
from health import health

class TyrianNavi(arcade.Window):
    def __init__(self):
        super().__init__ (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_sprite = None
        self.bullet_list = None
        self.enemy_list = None
        self.enemy_bullet_list = None
        self.time_since_last_spawn = 0
        self.explosion_list = None

        self.background = None
        self.shoot_sound = None
        self.explosion_sound = None

        self.health = None

    def setup(self):
        # Cargar la imagen del fondo y el sonido del disparo
        self.background = arcade.load_texture("img/fondo.png")
        self.shoot_sound = arcade.load_sound("Sounds/laser.wav")
        self.explosion_sound = arcade.load_sound("Sounds/explosion.wav")

        # Crear el jugador
        self.player_sprite = Player()

        # Inicializar listas de balas y enemigos
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()

        # Configurar el health (vidas y puntaje)
        self.health = health(PLAYER_LIVES, 0)

    def spawn_enemy(self):
        enemy = Enemy()
        self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()

        # Dibujar el fondo
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Dibujar sprites
        self.player_sprite.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.explosion_list.draw()

        # Dibujar el HUD
        self.health.draw()

    def on_update(self, delta_time):
        if not self.health.game_over:
            self.player_sprite.update()
            self.bullet_list.update()
            self.enemy_list.update()
            self.enemy_bullet_list.update()
            self.explosion_list.update()

        # Controlar el tiempo para generar enemigos
        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= SPAWN_RATE:
            self.spawn_enemy()
            self.time_since_last_spawn = 0

        # Hacer que los enemigos disparen
        for enemy in self.enemy_list:
            if random.random() < 0.01:  # Probabilidad baja para no saturar de disparos
                bullet = enemy.shoot()
                self.enemy_bullet_list.append(bullet)

        self.check_collisions()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5
        elif key == arcade.key.UP:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -5
        elif key == arcade.key.SPACE:
            self.shoot_bullet()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_sprite.change_x = 0
        elif key in [arcade.key.UP, arcade.key.DOWN]:
            self.player_sprite.change_y = 0

    def shoot_bullet(self):
        # Reproducir el sonido de disparo
        arcade.play_sound(self.shoot_sound)

        # Crear y disparar una bala
        bullet = Bullet("img/B1.png", self.player_sprite)
        self.bullet_list.append(bullet)

    def check_collisions(self):
        # Verificar colisiones entre balas y enemigos
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    explosion = Explosion(enemy.center_x, enemy.center_y)
                    self.explosion_list.append(explosion)

                    arcade.play_sound(self.explosion_sound)

                    enemy.remove_from_sprite_lists()
                    self.health.update_score(10)  # Sumar puntos al destruir un enemigo

        # Verificar colisiones entre el jugador y balas de enemigos
        collided_enemies = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
        if collided_enemies:
        # Solo quitar una vida por colisión con una bala enemiga
            self.health.lose_life()
        # Eliminar las balas enemigas que colisionaron con el jugador
            # for enemy_bullet in self.enemy_bullet_list:
            #     if arcade.check_for_collision(self.player_sprite, enemy_bullet):
            #         enemy_bullet.remove_from_sprite_lists()
            for enemy_bullet in collided_enemies:
                enemy_bullet.remove_from_sprite_lists()


def main():
    window = TyrianNavi()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()