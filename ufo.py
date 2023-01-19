from random import choice

import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer


class Ufo(Sprite):
    def __init__(self, game, type=3):
        super().__init__()
        self.type = type
        self.sound = game.sound
        self.screen = game.screen

        # Randomize value, based on original scheme from 1980s SI
        self.points = choice([50, 100, 150, 200, 300])

        self.sb = game.scoreboard
        self.sound = game.sound
        self.settings = game.settings
        self.image = pg.image.load('images/ufo0.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.settings.ufo_speed_factor = 1
        self.dying = self.dead = False

        # Initialize timers
        ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(2)]
        self.timer_normal = Timer(image_list=ufo_images)
        ufo_explosion_images = [pg.image.load(
            f'images/ufoexplosion{n}.png') for n in range(3)]

        for image in range(7):
            ufo_explosion_images.append(pg.image.load(
                f'images/ufopoint{self.points}.png'))

        self.timer_explosion = Timer(
            image_list=ufo_explosion_images, is_loop=False, delay=200)
        self.timer = self.timer_normal

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.settings.ufo_speed_factor = 0
            self.timer = self.timer_explosion
            self.sound.ship_explosion()
            # Pass in optional parameter
            self.sb.increment_score(self.type, self.points)

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.ufo_speed_factor * settings.fleet_direction_ufo)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        self.sound.ufo_entrance()


class Ufos:
    def __init__(self, game):
        self.model_ufo = Ufo(game=game)
        self.game = game
        self.sb = game.scoreboard
        self.ufos = Group()
        self.ship_lasers = game.ship_lasers.lasers    # A laser Group
        self.screen = game.screen
        self.settings = game.settings
        self.ship = game.ship

    def reset(self):
        self.ufos.empty()

    def create_ufo(self, ufo_number=0, row_number=0):
        ufo = Ufo(game=self.game)
        ufo_width = ufo.rect.width

        # Seems counterintuitive, but we can adjust where we want the UFO later
        ufo.x = ufo_width + 1.5 * ufo_width * ufo_number
        ufo.rect.x = ufo.x
        ufo.rect.y = ufo.rect.height + 1.2 * ufo.rect.height * row_number
        self.ufos.add(ufo)

    def check_fleet_edges(self):
        for ufo in self.ufos.sprites():
            if ufo.check_edges():
                ufo.kill()
                ufo.dying = True
                break

    def check_fleet_bottom(self):
        for ufo in self.ufos.sprites():
            if ufo.check_bottom_or_ship(self.ship):
                self.ship.die()
                break

    def change_fleet_direction(self):
        self.settings.fleet_direction_ufo *= -1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(
            self.ufos, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()

    def update(self):
        if len(self.ufos.sprites()) == 1:
            self.check_fleet_edges()
            self.check_fleet_bottom()
            self.check_collisions()
            for ufo in self.ufos.sprites():
                if ufo.dead:  # Set True once the explosion animation has completed
                    ufo.remove()
                ufo.update()
