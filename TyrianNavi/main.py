import random
import arcade
from explosion import Explosion
from player import Player
from enemy import Enemy, FinalBoss
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, PLAYER_LIVES, SPAWN_RATE
from health import health

class TyrianNavi(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
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
        self.background_music = None  

        self.health = None
        self.win_phase = False
        self.final_boss = None
        self.boss_health = 100
        self.victory_message_shown = False

    def setup(self):
        self.background = arcade.load_texture("img/fondo.png")
        self.shoot_sound = arcade.load_sound("Sounds/laser.wav")
        self.explosion_sound = arcade.load_sound("Sounds/explosion.wav")

        self.background_music = arcade.load_sound("Sounds/music.mp3")
        arcade.play_sound(self.background_music, looping=True)  

        self.player_sprite = Player()

        # Inicializar listas de balas y enemigos
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()

        self.health = health(PLAYER_LIVES, 0)

    def spawn_enemy(self):
        if not self.win_phase:
            enemy = Enemy()
            self.enemy_list.append(enemy)

    def spawn_final_boss(self):
        self.final_boss = FinalBoss()
        self.enemy_list.append(self.final_boss)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_sprite.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.explosion_list.draw()

        if self.victory_message_shown:
            arcade.draw_text(
                "YOU WIN\nGracias por jugar TyrianNavi",
                self.width // 2, self.height // 2,
                arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center"
            )

        self.health.draw()

        if self.win_phase and self.final_boss:
            arcade.draw_text(f"Boss Health: {self.boss_health}", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, arcade.color.RED, 24, anchor_x="center")

    def on_update(self, delta_time):
        if not self.health.game_over and not self.victory_message_shown:
            self.player_sprite.update()
            self.bullet_list.update()
            self.enemy_list.update()
            self.enemy_bullet_list.update()
            self.explosion_list.update()

            if self.health.score >= 500 and not self.win_phase:
                self.win_phase = True
                arcade.schedule(self.start_final_level, 3)
            
            if self.win_phase and self.final_boss:
                self.final_boss.update()

            if self.boss_health <= 0:
                self.on_victory()
                return

            self.time_since_last_spawn += delta_time
            if self.time_since_last_spawn >= SPAWN_RATE and not self.win_phase:
                self.spawn_enemy()
                self.time_since_last_spawn = 0

            for enemy in self.enemy_list:
                if random.random() < 0.01:
                    bullet = enemy.shoot()
                    self.enemy_bullet_list.append(bullet)

            self.check_collisions()
 
    def start_final_level(self, delta_time):
        arcade.unschedule(self.start_final_level)
        self.spawn_final_boss()

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
        arcade.play_sound(self.shoot_sound)
        bullet = Bullet("img/B1.png", self.player_sprite)
        self.bullet_list.append(bullet)

    def check_collisions(self):
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
        
            if hit_list:
                bullet.remove_from_sprite_lists()

                for enemy in hit_list:
                    explosion = Explosion(enemy.center_x, enemy.center_y)
                    self.explosion_list.append(explosion)
                    arcade.play_sound(self.explosion_sound)

                    if isinstance(enemy, FinalBoss):
                        self.boss_health -= 10
                        print(f"Boss health: {self.boss_health}")

                        if self.boss_health <= 0:
                            self.on_victory()

                    else:
                        enemy.remove_from_sprite_lists()
                        self.health.update_score(10)

        collided_enemies = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)

        if collided_enemies:
            self.health.lose_life()
            for enemy_bullet in collided_enemies:
                enemy_bullet.remove_from_sprite_lists()

    def on_victory(self):
        self.win_phase = False
        self.victory_message_shown = True
        arcade.schedule(self.end_game, 5)

    def end_game(self, delta_time):
        arcade.close_window()

def main():
    window = TyrianNavi()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
