import pygame
from settings import SCREEN_HEIGHT
from spritesheet import *
from settings import *
from timer import Timer
import copy

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, game, groups=[]):
        super().__init__(groups)
        self.game = game
        self.screen = game.screen
        self.vel_y = 0
        self.dx = 0
        self.dy = 0

    def check_hit_tile(self):
        c = copy.copy(self.rect)
        c.y += self.dy
        c2 = copy.copy(self.rect)
        c2.x += self.dx
        for tile in self.game.map.tiles.sprites():
            if tile.rect.colliderect(c2):
                if self.dx < 0:
                    self.rect.left = tile.rect.right
                    self.dx = 0
                elif self.dx > 0:
                    self.rect.right = tile.rect.left
                    self.dx = 0
            elif tile.rect.colliderect(c):
                if self.dy > 0:
                    self.num_jumps = 2
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.state = 'still'
                elif self.dy < 0:
                    self.state='jump'
                    self.num_jumps = 0
                    self.rect.top = tile.rect.bottom
                    self.dy = 0

class Player(Entity):
    def __init__(self, x, y, game, groups=[]):
        super().__init__(x, y, game, groups)
        self.spritesheet = MarioSpriteSheet()
        self.right = True

        self.stillimage = self.spritesheet.get_sprite('mario0')
        self.stillimage_left = self.spritesheet.get_sprite('mario0', True)

        delay = 200
        self.running_imgs = Timer(image_list=[self.spritesheet.get_sprite('mario1'), self.spritesheet.get_sprite('mario2')], delay=delay)
        self.running_imgs_left = Timer(image_list=[self.spritesheet.get_sprite('mario1', True), self.spritesheet.get_sprite('mario2', True)], delay=delay)

        self.jumpimage = self.spritesheet.get_sprite('mario3')
        self.jumpimage_left = self.spritesheet.get_sprite('mario3', True)

        self.right_imgs = {'still': self.stillimage, 'jump': self.jumpimage, 'run': self.running_imgs.image()}
        self.left_imgs = {'still': self.stillimage_left, 'jump': self.jumpimage_left, 'run': self.running_imgs_left.image()}
        self.state = 'jump'

        self.image = self.right_imgs[self.state]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jumping = False
        self.num_jumps = 0
        self.on_floor = False
        self.died = False

    def mario_run_animation(self):
        self.state = 'run'
        self.right_imgs[self.state] = self.running_imgs.image()
        self.left_imgs[self.state] = self.running_imgs_left.image()

    def jump(self):
        self.vel_y = -JUMP_SPEED
        self.jumping = True
        self.state = 'jump'
        self.num_jumps -= 1

    def handle_input(self):
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumping == False and self.num_jumps > 0:
            self.jump()
        if key[pygame.K_UP] == False:
            self.jumping = False
        if key[pygame.K_LEFT]:
            self.dx -= RUN_SPEED
            self.right = False
            if self.state != 'jump':
                self.mario_run_animation()
        elif key[pygame.K_RIGHT]:
            self.dx += RUN_SPEED
            self.right = True
            if self.state != 'jump':
                self.mario_run_animation()

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy += self.vel_y

    def handle_animation(self):
        self.image = self.right_imgs[self.state] if self.right else self.left_imgs[self.state]

    # not allowing movement past the left side of the screen
    # and the right side when we reach end of map.
    def handle_movement_x(self):
        if self.rect.right + self.dx > SCREEN_WIDTH/2 and not self.game.map.reached_end():
            self.rect.right = SCREEN_WIDTH/2
        if self.rect.right + self.dx > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.x + self.dx <= 0:
            self.rect.x = 0
        else:
            self.rect.x += self.dx
    
    def check_fall_off_map(self):
        return self.rect.y + self.dy >= SCREEN_HEIGHT

    def handle_movement_y(self):
        if self.check_fall_off_map():
            self.die()
        else:
            self.rect.y += self.dy

    def check_hit_bottom_tile(self, tile):
        if self.dy < 0 and self.rect.top < tile.rect.bottom:
            self.rect.top = tile.rect.bottom
            return True
        return False

    def die(self):
        self.died = True
        self.kill()
        print("Game over")

    def check_hit_enemy(self):
        c = copy.copy(self.rect)
        c.y += self.dy
        c2 = copy.copy(self.rect)
        c2.x += self.dx
        for goomba in self.game.map.goombas.sprites():
            if goomba.rect.colliderect(c2) and goomba.died == False:
                self.die()
            elif goomba.rect.colliderect(c):
                if c.bottom > goomba.rect.top:
                    self.rect.bottom = goomba.rect.top
                    self.jump()
                    goomba.die()

    def update(self):
        self.handle_input()
        self.handle_animation()
        # check for collisions
        # update player coords
        # if self.dx == 0 and self.dy == 0:
        #     self.state = 'still'
        # Restrict movement past screen
        self.check_hit_enemy()
        self.check_hit_tile()
        self.handle_movement_x()
        self.handle_movement_y()
        self.screen.blit(self.image, self.rect)
