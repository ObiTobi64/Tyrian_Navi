import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class health:
    def __init__(self, lives, score):
        self.lives = lives
        self.score = score
        self.game_over = False

    def draw(self):
        if self.game_over:
            arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                            arcade.color.RED, 54, anchor_x="center", anchor_y="center")
        else:
            arcade.draw_text(f"Lives: {self.lives}", 10, 20, arcade.color.WHITE, 14)
            arcade.draw_text(f"Score: {self.score}", SCREEN_WIDTH - 100, 20, arcade.color.WHITE, 14)

    def update_score(self, points):
        self.score += points

    def lose_life(self):
        if not self.game_over:
            self.lives -= 1
            if self.lives <= 0:
                self.lives = 0
                self.game_over = True

