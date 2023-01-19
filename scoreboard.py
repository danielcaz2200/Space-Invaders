import pygame as pg
import os.path
from ship import Ship


class Scoreboard:
    def __init__(self, game):
        self.score = 0
        self.game = game

        self.get_high_score()

        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont('arial', 48)
        self.score_font = pg.font.SysFont('arial', 38)

        self.score_image = None
        self.score_rect = None
        self.ships = None
        self.high_score = None
        self.high_score_image = None
        self.high_score_rect = None

        self.prep_score()
        self.prep_ships()
        self.prep_high_score()

    def increment_score(self, type, rand_points=None):  # Optional rand_points for UFO
        if type == 3:
            self.score += rand_points
        else:
            self.score += self.settings.alien_points[type]
        self.prep_score()

    def prep_score(self):
        score_str = f'Score: {self.score}'
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_ships(self, lives=3):
        self.ships = pg.sprite.Group()
        for ship_number in range(lives):
            ship = Ship(game=self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_high_score(self):
        self.get_high_score()
        score_str = f'High score: {self.high_score}'
        self.high_score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top middle of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.settings.screen_width // 2
        self.high_score_rect.top = 20

    def get_high_score(self):
        # Check if hiscore.txt already exists
        if os.path.exists('hiscore.txt'):
            with open('hiscore.txt', 'r') as f:
                high_score = int(f.readline())
                self.high_score = high_score
        else:
            self.high_score = 0  # Default if high score does not exist

    def set_high_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score
            with open('hiscore.txt', 'w') as f:
                # Write new high score, if better than last
                f.write(f'{self.high_score}')

    def reset(self):
        self.score = 0
        self.prep_score()
        self.update()

    def update(self):
        self.prep_high_score()
        self.draw()

    def draw(self):
        # Blit everything to the screen
        self.ships.draw(surface=self.screen)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
