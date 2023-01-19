import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(1.0)
        alienlaser_sound = pg.mixer.Sound('sounds/alienlaser.wav')
        alienlaser_sound.set_volume(1.0)
        player_laser = pg.mixer.Sound('sounds/shoot.wav')
        player_laser.set_volume(0.2)
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
        explosion_sound = pg.mixer.Sound('sounds/explosion.wav')
        explosion_sound.set_volume(0.3)
        ufo_sound = pg.mixer.Sound('sounds/ufo_lowpitch.wav')
        ufo_sound.set_volume(0.05)
        self.sounds = {'explosion': explosion_sound, 'alienlaser': alienlaser_sound, 'playerlaser': player_laser,
                       'gameover': gameover_sound, 'ufo': ufo_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def play_menu(self):
        pg.mixer.music.load('sounds/burning_memory.wav')
        pg.mixer.music.set_volume(1.0)
        self.play_bg()

    def speedup(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/bg_music_fast.wav')
        pg.mixer.music.set_volume(1.0)
        self.play_bg()

    def speedup_two(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/bg_music_fastest.wav')
        pg.mixer.music.set_volume(1.0)
        self.play_bg()

    def reset(self, bg_music='sounds/bg_music.wav'):
        self.stop_bg()
        pg.mixer.music.load(bg_music)
        self.play_bg()

    def stop_bg(self):
        pg.mixer.music.stop()

    def ufo_entrance(self):
        pg.mixer.Sound.play(self.sounds['ufo'])  # Used when ufo enters

    def ship_explosion(self):
        # Used when ufo or ship explodes
        pg.mixer.Sound.play(self.sounds['explosion'])

    def shoot_laser(self, type):
        pg.mixer.Sound.play(
            self.sounds['alienlaser' if type == LaserType.ALIEN else 'playerlaser'])  # Differentiate laser sounds

    def gameover(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
