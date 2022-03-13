from time import sleep

import pygame as pg
from pygame.sprite import Group

import game_functions as gf
from alien import AlienFleet
from GameStats import GameStats
from laser import LasersGroup
from settings import Settings
from ship import Ship
from landing_page import LandingPage
from scoreboard import Scoreboard
from barrier import Barriers
from sound import Sound

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
        self.barriers = Barriers(game=self)
        self.gameStats = GameStats(game=self)
        self.sound = Sound()

        self.sb = Scoreboard(game=self)
        self.active = True

    def restart(self):
        self.ship.reset()
        self.lasers.reset()
        self.aliens.respawn()

    def reset(self):
        self.ship.reset()
        self.lasers.reset()
        self.aliens.respawn()
        self.gameStats.level_up()

    def update(self):
        self.ship.update()
        self.lasers.update()
        self.aliens.update()
        self.sb.update()
        self.barriers.update()

    def draw(self):
        self.ship.draw()
        self.aliens.draw()
        self.sb.draw()
        self.barriers.draw()

    def play(self):
        finished = False
        self.sound.play_bg_2()
        while not finished:
            if self.active:
                self.update()
            else:
                self.sound.play_game_over()
            gf.update_screen(game=self)
            gf.check_events(game=self)


def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
