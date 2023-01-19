import pygame as pg


class StartScreen:
    def __init__(self, settings, screen, play_button, highscore_button):
        self.screen = screen
        self.settings = settings
        self.play_button = play_button
        self.highscore_button = highscore_button

        self.ufo = pg.image.load('images/ufo0.png')
        self.alien0 = pg.image.load('images/alien01.png')
        self.alien1 = pg.image.load('images/alien10.png')
        self.alien2 = pg.image.load('images/alien20.png')
        self.alien_rect = self.alien0.get_rect

        self.size = self.settings.screen_width, self.settings.screen_height

        self.menu_color = self.settings.bg_color
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont('arial', 48)

        self.size = (self.settings.screen_width, self.settings.screen_height)
        pg.display.flip()

    def draw(self, screen):
        screen.fill(self.menu_color)

        # Render text for 'SPACE'
        spacefont = pg.font.SysFont('arial', 100)
        spacetext = spacefont.render('SPACE', True, (255, 255, 255))
        spacetext_pos = spacetext.get_rect()
        spacetext_pos.centerx = self.size[0]/2

        # Render text for 'INVADERS'
        invadersfont = pg.font.SysFont('arial', 100)
        invaderstext = invadersfont.render("INVADERS", True, (0, 255, 0))
        invaders_pos = invaderstext.get_rect()
        invaders_pos.centerx = self.size[0]/2
        invaders_pos.centery = self.size[1]/6

        menutext0 = self.font.render(' = ??? MYSTERY', True, self.text_color)

        menutext1 = self.font.render(' = 10 PTS', True, self.text_color)

        menutext2 = self.font.render(' = 20 PTS', True, self.text_color)

        menutext3 = self.font.render(' = 40 PTS', True, self.text_color)

        # Position top, middle and low aliens
        menutext0_pos = ((self.size[0] / 2) - 50, (self.size[1] / 2)-200)
        ufo_pos = ((self.size[0] / 2)-105, (self.size[1] / 2)-215)

        menutext1_pos = ((self.size[0] / 2) - 50, (self.size[1] / 2) - 150)
        alien0_pos = ((self.size[0] / 2) - 100, (self.size[1] / 2) - 155)

        menutext2_pos = ((self.size[0] / 2) - 50, (self.size[1] / 2) - 100)
        alien1_pos = ((self.size[0] / 2) - 100, (self.size[1] / 2) - 105)

        menutext3_pos = ((self.size[0]/2)-50, (self.size[1])/2-50)
        alien2_pos = ((self.size[0] / 2) - 100, (self.size[1] / 2) - 55)

        # Blit everything to the screen
        screen.blit(spacetext, spacetext_pos)
        screen.blit(invaderstext, invaders_pos)

        screen.blit(self.ufo, ufo_pos)
        screen.blit(menutext0, menutext0_pos)

        screen.blit(self.alien0, alien0_pos)
        screen.blit(menutext1, menutext1_pos)

        screen.blit(self.alien1, alien1_pos)
        screen.blit(menutext2, menutext2_pos)

        screen.blit(self.alien2, alien2_pos)
        screen.blit(menutext3, menutext3_pos)

        self.play_button.draw()
        self.highscore_button.draw()

        pg.display.flip()
