import sys
from math import ceil

import pygame as pg
from vector import Vector
from laser import Laser
from alien import Alien

LEFT, RIGHT, UP, DOWN, STOP, FIRE = 'left', 'right', 'up', 'down', 'stop', 'fire'
dirs = {LEFT: Vector(-1, 0), RIGHT: Vector(1, 0),
        UP: Vector(0, -1), DOWN: Vector(0, 1), STOP: Vector(0, 0)}
dir_keys = {pg.K_LEFT: LEFT, pg.K_a: LEFT, pg.K_RIGHT: RIGHT, pg.K_d: RIGHT,
            pg.K_UP: UP, pg.K_w: UP, pg.K_DOWN: DOWN, pg.K_s: DOWN}
fire_key = {pg.K_SPACE: FIRE}


def check_keydown_events(e, game, speed):
    if e.key in dir_keys:
        v = dirs[dir_keys[e.key]] * speed
        game.ship.inc_add(v)
    elif e.key in fire_key:
        game.ship.hold_fire_on()
    elif e.key == pg.K_ESCAPE:
        sys.exit()


def check_keyup_events(e, game, speed):
    if e.key in dir_keys:
        v = dirs[dir_keys[e.key]] * speed
        game.ship.inc_add(-v)
    elif e.key in fire_key:
        game.ship.hold_fire_off()


def larger_abs(num):
    return ceil(num) if num > 0 else -1 * ceil(abs(num))


def check_events(game):
    speed = larger_abs(game.settings.ship_speed_factor)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        elif e.type == pg.KEYDOWN:
            check_keydown_events(e, game, speed)
        elif e.type == pg.KEYUP:
            check_keyup_events(e, game, speed)


# def create_alien(game, alien_width, i):
#     alien = Alien(game)
#     alien.x = alien_width + 2 * alien_width * i
#     alien.rect.x = alien.x
#     game.aliens.add(alien)


# def create_fleet(game):
#     alien = Alien(game)
#     alien_width = alien.rect.width
#     num_aliens_x = get_num_aliens_x(game, alien_width)
#     for i in range(num_aliens_x):
#         create_alien(game, alien_width, i)


def update_screen(game):
    game.screen.blit(game.settings.bg_image, (0,0))
    game.ship.draw()
    game.lasers.draw()
    game.aliens.draw()
    pg.display.flip()
