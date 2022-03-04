from time import sleep

import pygame as pg

from pygame.sprite import Group

import game_functions as gf
from alien import AlienFleet
from GameStats import GameStats
from laser import LasersGroup
from settings import Settings
from ship import Ship


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.lasers = LasersGroup(game=self)
        self.aliens = AlienFleet(game= self)
        self.gameStats = GameStats(game=self)

        self.active = True

    def reset(self):
        self.ship.reset()
        self.lasers.reset()
        self.aliens.respawn()
        self.gameStats.lost_ship()
        # pg.time.wait(1000)

    def update(self):
        self.ship.update()
        self.lasers.update()
        self.aliens.update()

    def draw(self):
        self.ship.draw()
        self.aliens.draw()

    def play(self):
        finished = False
        while not finished:
            if self.active:
                self.update()
            gf.update_screen(game=self)
            gf.check_events(game=self)


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
