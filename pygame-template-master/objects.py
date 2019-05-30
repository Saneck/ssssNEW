import pygame as pg
from settings import *
import random


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\sprites\\player.gif")
        self.rect = self.image.get_rect()
        self.direction = 1
        self.vel_x = 0
        self.vel_y = 0
        self.rect.x = 20
        self.rect.y = 100
        self.can_jump = True
        self.can_shoot = True
        self.reload_ticks = 0


    def update(self):
        keys = pg.key.get_pressed()
        mousekeys = pg.mouse.get_pressed()
        if keys[pg.K_a]:
            self.vel_x = -SPEED
            self.direction = -1
        if keys[pg.K_d]:
            self.vel_x = +SPEED
            self.direction = 1
        if keys[pg.K_SPACE] and self.can_jump:
            self.vel_y -= PLAYER_JUMP
            self.can_jump = False
        if pg.time.get_ticks()-self.reload_ticks > self.weapon.reload:
            self.can_shoot = True
        if mousekeys[0] and self.can_shoot:
            event = pg.event.Event(SHOT_FIRED)
            pg.event.post(event)
            self.reload_ticks = pg.time.get_ticks()
            self.can_shoot = False
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_x = 0



    def draw(self, canvas):
        canvas.blit(self.image, self.rect)

class Platform(pg.sprite.Sprite):
    def __init__(self, img_path, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        self.enemy_score = 0
        pg.sprite.Sprite.__init__(self)
        if random.choice([True, False]):
            self.image = pg.image.load("img\\sprites\\tree.gif")
            self.image = pg.transform.scale(self.image, (50, 50))
            self.speed = 1.5
            self.hp = 50
        else:
            self.image = pg.image.load("img\\sprites\\croc.gif")
            self.image =  pg.transform.scale(self.image, (20, 20))
            self.speed = 1.5
            self.hp = 50
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 10)
        self.direction = random.choice([-1,1])
        self.vel_y = 0
    def update(self):
        self.vel_y += GRAVITY
        self.rect.x += self.speed * self.direction
        self.rect.y += self.vel_y


class Bullet(pg.sprite.Sprite):
    def __init__(self, x , y, dir_x, dir_y, weapon):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\smallbullet.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = weapon.bullet_speed
        self.damage = weapon.damage
    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

class Weapon(pg.sprite.Sprite):
    def __init__(self, damage, bullet_speed, reload, name, img, player):
        pg.sprite.Sprite.__init__(self)
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.reload = reload
        self.name = name
        self.image = pg.Surface((200,114), pg.SRCALPHA, 32)
        self.image.blit(pg.image.load("img\\sprites\\pistolRIGHT.png").convert_alpha(), (0,0), (0, 0, 200, 114))
        self.image = pg.transform.scale(self.image, (20,12))
        self.rect = self.image.get_rect()
        self.player = player
    def draw(self, canvas):
        canvas.blit(self.image, self.rect)

    def update(self):
        self.rect.x = self.player.rect.x + 25
        self.rect.y = self.player.rect.y + 14

class Crate(pg.sprite.Sprite):
    def __init__(self, spawn_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\crate.png")
        self.rect = self.image.get_rect()
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]
