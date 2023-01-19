import sys
import pygame as pg
from vector import Vector
from random import randint

# Velocity vector dictionary
movement = {
    pg.K_LEFT: Vector(-1, 0),
    pg.K_RIGHT: Vector(1, 0),
}


def check_keydown_events(event, settings, ship):
    key = event.key
    if key == pg.K_SPACE:
        ship.shooting = True
    elif key in movement.keys():
        ship.vel = settings.ship_speed_factor * movement[key]


def check_keyup_events(event, ship):
    key = event.key
    if key == pg.K_SPACE:
        ship.shooting = False
    elif key == pg.K_ESCAPE:
        ship.vel = Vector()   # Note: Escape key stops the ship
    elif key in movement.keys():
        ship.vel = Vector()


def check_play_button(game, mouse_pos):
    pressed = game.play_button.msg_image_rect.collidepoint(mouse_pos)
    if pressed and not game.settings.game_active:
        game.settings.game_active = True
        game.settings.highscore_active = False
        pg.mouse.set_visible(False)

        # Resets score and all game attributes
        game.reset()


def check_high_score_button(game, mouse_pos):
    pressed = game.highscore_button.msg_image_rect.collidepoint(mouse_pos)
    if pressed and not game.settings.game_active:  # Activate high score menu
        game.settings.highscore_active = True


def check_events(game, settings, ship, ufos):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, settings=settings, ship=ship)
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event, ship=ship)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0], event.pos[1])
            check_play_button(game=game, mouse_pos=mouse_pos)
            check_high_score_button(game=game, mouse_pos=mouse_pos)
        elif event.type == pg.USEREVENT+0 and settings.game_active:  # User event for random UFO
            ufos.create_ufo()
            # Reset event timer
            game.settings.ufo_speed_factor = 1
            # pg.time.set_timer(pg.USEREVENT+0, randint(5000, 15000))


def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = max(0, min(top, settings.screen_height - height))

    # Clamps player to the screen
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)
