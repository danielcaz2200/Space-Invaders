# Developed by Daniel Cazarez
# and Ethan Bockler
# for CPSC 386 - Mccarthy Wednesday Night

from random import randint
from button import Button
import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers

from startscreen import StartScreen
from highscorescreen import HighScoreScreen
from ufo import Ufos


class Game:
    def __init__(self):
        """Initializes all game attributes"""
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # A tuple
        self.screen = pg.display.set_mode(size=size)
        self.bg_image = pg.transform.scale(
            pg.image.load('images/background.jpg'), (1200, 800))
        pg.display.set_caption(
            "Modified Space Invaders by Daniel Cazarez and Ethan Bockler")
        self.sound = Sound(bg_music="sounds/bg_music.wav")
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(
            settings=self.settings, type=LaserType.ALIEN)
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.scoreboard = Scoreboard(game=self)
        self.aliens = Aliens(game=self)
        self.ufos = Ufos(game=self)
        self.settings.initialize_speed_settings()
        self.play_button = Button(screen=self.screen, msg="PLAY")
        self.highscore_button = Button(screen=self.screen, msg="HIGH SCORE")
        self.highscore_button.reposition_y(50)
        self.high_score_screen = HighScoreScreen(
            settings=self.settings, screen=self.screen, play_button=self.play_button, sb=self.scoreboard)
        self.start_screen = StartScreen(settings=self.settings, screen=self.screen, play_button=self.play_button,
                                        highscore_button=self.highscore_button)
        self.menu_music_playing = False

    def reset(self):
        print('Resetting game...\n')
        self.ship.reset()
        self.ufos.reset()
        self.aliens.reset()
        self.ship_lasers.reset()
        self.alien_lasers.reset()
        self.barriers.reset()
        self.scoreboard.prep_ships(lives=self.ship.ships_left)
        self.sound.reset()

    def game_over(self):
        print('All ships gone: game over!\n')
        self.ship.timer.index = 0
        self.sound.gameover()
        self.scoreboard.set_high_score()
        self.scoreboard.reset()
        self.settings.game_active = False
        self.ship.ships_left = self.settings.ship_limit
        self.sound.stop_bg()
        pg.mouse.set_visible(True)

    def background(self):
        self.screen.blit(self.bg_image, (0, 0))

    def play(self):
        # Set original event timer for UFO event
        pg.time.set_timer(pg.USEREVENT+0, randint(10000, 15000))
        while True:
            gf.check_events(game=self, settings=self.settings,
                            ship=self.ship, ufos=self.ufos)

            if self.settings.game_active:
                self.menu_music_playing = False
                self.background()  # Displays space background
                self.ship.update()
                self.ufos.update()
                self.aliens.update()
                self.barriers.update()
                self.scoreboard.update()
            elif not self.settings.game_active:
                if not self.settings.highscore_active:
                    self.start_screen.draw(screen=self.screen)
                    if not self.menu_music_playing:
                        # Special/credits thanks to Bonbie on YouTube
                        # Credit: https://www.youtube.com/watch?v=oxiaILKjuc0&t=0s
                        self.sound.play_menu()
                        self.menu_music_playing = True
                else:
                    self.high_score_screen.draw(screen=self.screen)
            pg.display.flip()


def main():
    g = Game()
    g.play()  # Will run the game


if __name__ == '__main__':
    main()
