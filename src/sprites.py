# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class SpriteSheet:
    def __init__(self, filepath):
        self.spritesheet = pg.image.load(filepath)

    def get_image(self, x, y, w, h):
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pg.transform.scale(image, (w//2, h//2))        # Scaling images
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.was_right = True
        self.current_frame = 0
        self.last_update = 0
        self.load_char_images()
        self.image = self.game.char_spritesheet.get_image(0, 0, 64, 64)
        self.image.set_colorkey(IMG_BGCOLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)  # Starting position
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jump_counter = 0

    def load_char_images(self):
        self.idle_frames_r = [
            self.game.char_spritesheet.get_image(0, 0, 64, 64),
            self.game.char_spritesheet.get_image(64, 0, 64, 64),
        ]
        self.walking_frames_r = [
            self.game.char_spritesheet.get_image(128, 0, 64, 64),
            self.game.char_spritesheet.get_image(192, 0, 64, 64),
        ]

        self.idle_frames_l = [pg.transform.flip(frame, True, False) for frame in self.idle_frames_r]
        self.walking_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walking_frames_r]
        self.jump_frame = self.game.char_spritesheet.get_image(128, 0, 64, 64)

        for frame in self.idle_frames_l + self.idle_frames_r + self.walking_frames_l + self.walking_frames_r + [self.jump_frame]:
            frame.set_colorkey(IMG_BGCOLOR)

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platorms, False)
        self.rect.y -= 1
        if hits:
            self.jump_counter = 0
        if self.jump_counter < PLAYER_JUMPS:
            self.jump_counter += 1
            self.vel.y = -PLAYER_JUMP_VEL

    def update(self):
        self.char_animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        # Out of bounds restriction (x-axis)
        # TODO change to new (to be made) map system
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
        elif self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2

        self.rect.midbottom = self.pos

    def char_animate(self):
        tick = pg.time.get_ticks()
        self.walking = self.vel.x != 0
        self.jumping = self.vel.y != 0

        # if self.jumping:
        #     old_bottom = self.rect.bottom
        #     self.image = self.jump_frame
        #     self.rect = self.image.get_rect()
        #     self.rect.bottom = old_bottom

        if not self.jumping and self.walking:   # Player is walking
            if tick - self.last_update > 200 or (self.vel.x > 0 and not self.was_right or self.vel.x <= 0 and self.was_right):
                self.last_update = tick
                self.current_frame = (self.current_frame + 1) % 2
                old_bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                    self.was_right = True
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                    self.was_right = False
                self.rect = self.image.get_rect()
                self.rect.bottom = old_bottom

        if not self.jumping and not self.walking:   # Player is idle
            if tick - self.last_update > 800:
                self.last_update = tick
                self.current_frame = (self.current_frame + 1) % 2
                old_bottom = self.rect.bottom
                if self.was_right:
                    self.image = self.idle_frames_r[self.current_frame]
                else:
                    self.image = self.idle_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = old_bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(pg.sprite.Sprite):   # An impassable object
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pg.sprite.Sprite):  # Immovable death object
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Projectile(pg.sprite.Sprite):  # A movable Projectile
    def __init__(self, x, y, r, color, vel):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((r, r))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
