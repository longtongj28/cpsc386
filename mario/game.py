import pygame as pg
import sys
from settings import Settings

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        pg.display.set_caption("Mario")

    def update(self):
        # self.screen.blit(self.settings.bg_image, (0,0))
        self.screen.fill((230,230,230))
        self.detect_events()
        pg.display.flip()

    def detect_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()

    def play(self):
        while True:
            
            self.update()
            # gf.check_events(game=self)



def main():
    g = Game()
    # lp = LandingPage(game=g)
    # lp.show()
    g.play()

if __name__ == '__main__':
    main()
