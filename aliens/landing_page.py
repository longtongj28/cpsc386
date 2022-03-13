import pygame as pg
import sys
from alien import Alien
from button import Button
from sound import Sound
YELLOW = (155, 135, 12)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)


class LandingPage:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.landing_page_finished = False
        self.highscore = self.game.gameStats.get_highscore()

        headingFont = pg.font.SysFont(None, 192)
        subheadingFont = pg.font.SysFont(None, 122)
        font = pg.font.SysFont(None, 48)

        strings = [('SPACE', WHITE, headingFont), ('INVADERS', YELLOW, subheadingFont),
                   ('= 10 PTS', GREY, font), ('= 20 PTS', GREY, font),
                   ('= 40 PTS', GREY, font), ('= ???', GREY, font), (f'HIGH SCORE = {self.highscore}', GREY, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [75, 175]
        top_pos_scores = 275
        alien = [80 * x + top_pos_scores for x in range(2)]
        others = [80 * 2 + top_pos_scores + 40, 80*2+top_pos_scores + 150]
        alien.extend(others)
        play_high = [760]
        self.posns.extend(alien)
        self.posns.extend(play_high)

        centerx = self.screen.get_rect().centerx
        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        self.aliens = [Alien(game=self.game, alien_type="alienOne"),
                       Alien(game=self.game, alien_type="alienTwo"),
                       Alien(game=self.game, alien_type="alienThree"),
                       Alien(game=self.game, alien_type="alienFour")]
        self.aliens_pos = [(centerx - 200, alien[0]-15),
                           (centerx - 200, alien[1]-35),
                           (centerx - 200, alien[2]-55),
                           (centerx - 160, alien[3]-10)]
        self.play_button = Button(self.screen, "PLAY GAME", ul=(centerx-110, 650))
        self.sound = Sound()
        self.sound.play_bg()

    def get_text(self, font, msg, color):
        return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def detect_mouse_over(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.play_button.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.KEYUP and e.key == pg.K_p:  # pretend PLAY BUTTON pressed
                self.landing_page_finished = True  # TODO change to actual PLAY button
                # SEE ch. 14 of Crash Course for button
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.detect_mouse_over():
                    self.landing_page_finished = True
            elif e.type == pg.MOUSEMOTION:
                if self.detect_mouse_over():
                    self.play_button.hovered = True
                    self.play_button.change_color()
                else:
                    self.play_button.hovered = False
                    self.play_button.change_color()

    def show(self):
        while not self.landing_page_finished:
            self.draw()
            self.check_events()  # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw_aliens(self):
        for i in range(4):
            alien = self.aliens[i]
            x = self.aliens_pos[i][0]
            y = self.aliens_pos[i][1]
            alien.change_pos(x, y)
            alien.draw()
            alien.handle_animation()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text()
        self.draw_aliens()
        self.play_button.draw()
        # self.alien_fleet.draw()   # TODO draw my aliens
        # self.lasers.draw()        # TODO dray my button and handle mouse events
        pg.display.flip()
