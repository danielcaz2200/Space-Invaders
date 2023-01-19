import pygame as pg


class HighScoreScreen:
    def __init__(self, settings, screen, play_button, sb):
        self.screen = screen
        self.settings = settings
        self.play_button = play_button
        self.sb = sb

        self.size = self.settings.screen_width, self.settings.screen_height
        self.font = pg.font.SysFont('arial', 48)

        self.menu_color = self.settings.bg_color
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont('arial', 48)
        self.score_font = pg.font.SysFont('arial', 100)

        self.size = (self.settings.screen_width, self.settings.screen_height)
        pg.display.flip()

    def draw(self, screen):
        screen.fill(self.menu_color)

        # Render high score text
        highscoretext = self.font.render(
            'CURRENT HIGH SCORE:', True, self.text_color)

        highscorewidth = highscoretext.get_size()[0]
        highscoretext_pos = (
            (self.size[0] / 2)-(highscorewidth/2), (self.size[1] / 2)-200)

        # Render value text
        value = self.score_font.render(
            f'{self.sb.high_score}', True, self.text_color)
        valuewidth = value.get_size()[0]
        value_pos = ((self.size[0] / 2)-(valuewidth/2), (self.size[1] / 2)-100)

        # Blit everything
        screen.blit(highscoretext, highscoretext_pos)
        screen.blit(value, value_pos)
        self.play_button.draw()

        pg.display.flip()
