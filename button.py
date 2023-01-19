import pygame as pg


class Button:
    def __init__(self, screen, msg):
        """Button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (0, 255, 0)
        self.font = pg.font.SysFont('arial', 48)

        self.msg_image = self.font.render(
            msg, True, self.text_color, (0, 0, 0))
        self.msg_image_rect = self.msg_image.get_rect()

        self.msg_image_rect.centerx = self.screen_rect.centerx
        self.msg_image_rect.centery = self.screen_rect.centery + 50

    def draw(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def reposition_x(self, value):
        self.msg_image_rect.centerx += value

    def reposition_y(self, value):
        self.msg_image_rect.centery += value
