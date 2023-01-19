from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer


class Alien(Sprite):
    def __init__(self, game, type=0):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.sb = game.scoreboard

        # Alien classification
        self.type = type

        # Alien's death status
        self.dying = self.dead = False

        # Determine type and normal timer
        if type == 0:
            alien_images = [pg.image.load(
                f'images/alien0{n}.png') for n in range(3)]
            alien_explosion_images = [pg.transform.scale(pg.image.load(
                f'images/alien0explosion{n}.png'), (60, 60)) for n in range(5)]
        elif type == 1:
            alien_images = [pg.image.load(
                f'images/alien1{n}.png') for n in range(3)]
            alien_explosion_images = [pg.transform.scale(pg.image.load(
                f'images/alien1explosion{n}.png'), (60, 60)) for n in range(5)]
        elif type == 2:
            alien_images = [pg.image.load(
                f'images/alien2{n}.png') for n in range(3)]
            alien_explosion_images = [pg.transform.scale(pg.image.load(
                f'images/alien2explosion{n}.png'), (60, 60)) for n in range(5)]

        # Instantiate timers
        self.timer_normal = Timer(alien_images)
        self.timer = self.timer_normal
        self.timer_explosion = Timer(
            image_list=alien_explosion_images, is_loop=False)

        # Example alien images
        self.image = pg.image.load('images/alien01.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion

            self.sb.increment_score(self.type)

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sound = game.sound
        self.sb = game.scoreboard
        self.aliens = Group()

        # Create member attributes for ship lasers
        # and alien lasers
        self.ship_lasers = game.ship_lasers.lasers
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.ship = game.ship
        self.first_speed_up = False
        self.second_speed_up = False
        self.shoot_requests = 0
        self.create_fleet()

    def reset(self):
        self.aliens.empty()
        self.create_fleet()
        self.first_speed_up = False
        self.second_speed_up = False

    def create_alien(self, game, alien_number, row_number):
        if row_number == 1 or row_number == 2:
            alien = Alien(game, type=1)
        elif row_number == 0:
            alien = Alien(game, type=2)
        else:
            alien = Alien(game, type=0)
        alien_width = alien.rect.width
        alien.x = alien_width + 1.2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * \
            row_number + 50
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = 11
        number_rows = 5

        # Create fleet of aliens
        for row in range(number_rows):
            for alien in range(number_aliens_x):
                self.create_alien(
                    game=self.game, alien_number=alien, row_number=row)

    def check_music(self):
        if len(self.aliens.sprites()) == 30 and not self.first_speed_up:
            self.sound.speedup()
            self.first_speed_up = True
        if len(self.aliens.sprites()) == 15 and not self.second_speed_up:
            self.sound.speedup_two()
            self.second_speed_up = True

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(
            self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()

        collisions = pg.sprite.spritecollide(
            self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

        collisions = pg.sprite.groupcollide(
            self.aliens_lasers.lasers, self.ship_lasers, False, True)
        if collisions:
            for alien_lasers in collisions:
                alien_lasers.hit()

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        # Handle random generation of lasers from aliens
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(
                    game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.check_music()
        for alien in self.aliens.sprites():
            # set True once the explosion animation has completed
            if alien.dead:
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()
