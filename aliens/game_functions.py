import sys
from math import ceil

import pygame as pg
from vector import Vector
from game import Laser, Alien

LEFT, RIGHT, UP, DOWN, STOP, FIRE = 'left', 'right', 'up', 'down', 'stop', 'fire'
dirs = {LEFT: Vector(-1, 0), RIGHT: Vector(1, 0),
        UP: Vector(0, -1), DOWN: Vector(0, 1), STOP: Vector(0, 0)}
dir_keys = {pg.K_LEFT: LEFT, pg.K_a: LEFT, pg.K_RIGHT: RIGHT, pg.K_d: RIGHT,
            pg.K_UP: UP, pg.K_w: UP, pg.K_DOWN: DOWN, pg.K_s: DOWN}
fire_key = {pg.K_SPACE: FIRE}


def larger_abs(num):
    return ceil(num) if num > 0 else -1 * ceil(abs(num))


def fire_laser(game):
    if len(game.lasers) < game.settings.lasers_allowed:
        new_laser = Laser(game)
        game.lasers.add(new_laser)


def check_keydown_events(e, game, speed):
    if e.key in dir_keys:
        v = dirs[dir_keys[e.key]] * speed
        game.ship.inc_add(v)
    elif e.key in fire_key:
        fire_laser(game)
    elif e.key == pg.K_ESCAPE:
        sys.exit()


def check_keyup_events(e, game, speed):
    if e.key in dir_keys:
        v = dirs[dir_keys[e.key]] * speed
        game.ship.inc_add(-v)


def check_events(game):
    speed = larger_abs(game.settings.ship_speed_factor)
    ship = game.ship

    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        elif e.type == pg.KEYDOWN:
            check_keydown_events(e, game, speed)
        elif e.type == pg.KEYUP:
            check_keyup_events(e, game, speed)


def manage_lasers(game):
    for laser in game.lasers.copy():
        if laser.rect.bottom <= 0:
            game.lasers.remove(laser)


def get_num_aliens_x(game, alien_width):
    available_space_x = game.settings.screen_width - 2 * alien_width
    num_aliens_x = int(available_space_x / (2 * alien_width))
    return num_aliens_x


def create_alien(game, alien_width, i):
    alien = Alien(game)
    alien.x = alien_width + 2 * alien_width * i
    alien.rect.x = alien.x
    game.aliens.add(alien)


def create_fleet(game):
    alien = Alien(game)
    alien_width = alien.rect.width
    num_aliens_x = get_num_aliens_x(game, alien_width)
    for i in range(num_aliens_x):
        create_alien(game, alien_width, i)


def update_screen(game):
    game.screen.fill(game.bg_color)
    game.ship.draw()

    for alien in game.aliens.sprites():
        alien.draw()

    for laser in game.lasers.sprites():
        laser.draw()

    pg.display.flip()
