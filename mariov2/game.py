import pygame

from pygame.locals import *
from player import Player
from settings import *
from map import Map
from sound import Sound

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mario")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assets = pygame.sprite.Group()
        self.player = Player(100, 0, game=self, groups=[self.assets])
        self.map = Map(game=self)
        self.sound = Sound()

    def update(self):
        self.map.update()
        self.assets.update()

    def run(self):
        clock = pygame.time.Clock()
        run = True
        self.sound.play_bg()
        while run:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
            clock.tick(60)

        pygame.quit()

def main():
    g = Game()
    g.run()

if __name__ == '__main__':
    main()
