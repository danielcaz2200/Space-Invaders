import pygame as pg
from pygame.sprite import Sprite, Group


class Block(Sprite):
    shape = [
        '  xxxxxxx',
        ' xxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxx     xxx',
        'xx       xx'
    ]   # Shape will serve as an example to loop and enumerate through

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.color = (0, 255, 0)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Barriers:
    def __init__(self, game):
        self.blocks = Group()
        self.ship_lasers = game.ship_lasers.lasers
        self.aliens_lasers = game.alien_lasers.lasers
        self.width = game.settings.screen_width/10
        self.height = 2.0 * self.width / 4.0
        self.top = game.settings.screen_height - 2.1 * self.height
        self.screen = game.screen
        self.shape = Block.shape
        self.block_size = 12
        self.create_obstacles(x_start=0, y_start=self.top)

    def reset(self):
        self.blocks.empty()
        self.create_obstacles(x_start=0, y_start=self.top)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + (col_index * self.block_size + offset_x)
                    y = y_start + (row_index * self.block_size)
                    block = Block(self.block_size, x, y)
                    self.blocks.add(block)

    def create_obstacles(self, x_start, y_start):
        for n in range(4):
            offset_x = n * 2 * self.width + 1.5 * self.width
            self.create_obstacle(
                x_start=x_start, y_start=y_start, offset_x=offset_x)

    def draw(self):
        self.blocks.draw(self.screen)

    def check_collisions(self):
        # Check collisions between both the alien lasers and ship lasers
        pg.sprite.groupcollide(self.blocks, self.aliens_lasers, True, True)
        pg.sprite.groupcollide(self.blocks, self.ship_lasers, True, True)

    def update(self):
        self.check_collisions()
        self.draw()
