import arcade

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Invaders"

PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
BULLET_OFFSET = 20
SPAWN_RATE = 1.0  

class SpaceInvaders(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_sprite = None
        self.bullet_list = None
        self.enemy_list = None
        self.score = 0
        self.lives = 3
        self.enemy_direction = 1  
        self.enemy_positions = []  
        self.time_since_last_spawn = 0  

    def setup(self):
        self.player_sprite = arcade.Sprite("SpaceInvaders/img/A1.png")
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.bottom = 10

        
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

    
        for x in range(100, SCREEN_WIDTH - 100, 60):
            for y in range(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 300, -60):
                self.enemy_positions.append((x, y))

    def spawn_enemy(self):
        
        if self.enemy_positions:
            pos_x, pos_y = self.enemy_positions.pop(0)
            enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png")
            enemy.center_x = pos_x
            enemy.center_y = pos_y
            self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()

        self.player_sprite.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 700, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.bullet_list.update()

        for bullet in self.bullet_list:
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            enemy.center_x += ENEMY_SPEED * self.enemy_direction
            if enemy.right > SCREEN_WIDTH or enemy.left < 0:
                self.enemy_direction *= -1  
                for e in self.enemy_list:
                    e.center_y -= 30  
                break

    
        self.check_collisions()


        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.player_sprite, enemy):
                self.lives -= 1
                if self.lives <= 0:
                    print("Game Over")
                    self.close()

        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= SPAWN_RATE:
            self.spawn_enemy()
            self.time_since_last_spawn = 0

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_SPEED    
        elif key == arcade.key.SPACE:
            self.shoot_bullet()

    def on_key_release(self, key,  modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def shoot_bullet(self):
        
        bullet = arcade.Sprite("SpaceInvaders/img/B1.png")
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top + BULLET_OFFSET
        bullet.change_y = BULLET_SPEED
        self.bullet_list.append(bullet)

    def check_collisions(self):
        # Revisar colisiones entre balas y enemigos
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.score += 10


def main():
    window = SpaceInvaders()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
