import pygame as pg
import random
from settings import *
from objects import *

"""
Основной класс игры
Состояние игры описывается двумя переменными: running и playing. Если игра
running, то это означает, что приложение работает и игрок будет начинать новую
игру - new() снова и снова. Если игра playing, то в данный момент крутится основной игровой
цикл run() - это происходит внутри new()
"""
class Game:
    """
    Инициализируем pygame, создаем дисплей, название игры, часы и задаем изнчальное
    состояние игры: running = True, загружаем шрифт
    """
    def __init__(self):
        pg.init()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game name")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.bg_image = pg.transform.scale(pg.image.load("img\\space.png"),(1100,HEIGHT))


    """
    В этом методе реализуется логика новый игры, обнуляем счет, задаем начальные
    положения врагов, игрока и др.
    """
    def new(self):
        self.score = 0
        self.player = Player()
        self.bullets = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.crates = pg.sprite.Group()
        self.weapons = []
        self.enemies.add(Enemy())
        self.crates.add(Crate((100, 100)))
        self.crates_spawn_positions = [(100, 110), (320, 350), (600, 510), (60, 410), (500, 200)]
        self.weapons.append(Weapon(13, 5, 450, "pistol", "img\\sprites\\pistolRIGHT.png", self.player))
        self.weapons.append(Weapon(70, 12, 900, "sniper", "img\\sprites\\awpRIGHT.png", self.player))
        # self.weapons.append(Weapon(30, 9, 200, "akm", "img\\sprites\\akmRIGHT.png", self.player))
        self.player.weapon = Weapon(13, 5, 450, "pistol", "img\\sprites\\pistolRIGHT.png", self.player)
        self.enemy_spawn_time = 3000
        self.enemy_counter = 1
        pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
        self.ptfm()
        self.playing = True
        while self.playing:
            self.run()

    """
    Обновляем положение игровых объеков
    """

    def update(self):
        self.player.weapon.update()
        self.player.update()
        self.platforms.update()
        self.enemies.update()
        self.bullets.update()
        self.crates.update()
        self.check_collision()
        for enemy in self.enemies:
            if enemy.rect.y > 570:
                enemy.rect.y = 2
                enemy.enemy_score += 1
                enemy.speed = enemy.speed * 2
                if enemy.enemy_score == 2:
                    enemy.speed = 1.5



    """
    Основная функция, в которой реализуется цикл анимации:
    1.Проверяем события
    2.Обновляем положение игровых объектов
    3.Закрашиваем экран цветом заднего фона
    4.Отрисовываем объекты заново
    """
    def run(self):
        self.clock.tick(60)
        self.events()
        self.update()
        self.fill()
        self.draw()


    def ptfm(self):
        self.platforms.add(Platform("img\\smallplatform.png", 2, 325))
        self.platforms.add(Platform("img\\smallplatform.png", 540, 325))

        self.platforms.add(Platform("img\\smallplatform.png", 265, 130))

        self.platforms.add(Platform("img\\smallplatform.png", 115, 460))
        self.platforms.add(Platform("img\\smallplatform.png", 400, 460))

        self.platforms.add(Platform("img\\bigplatform.png", -28, 551))
        self.platforms.add(Platform("img\\bigplatform.png", 422, 551))

        self.platforms.add(Platform("img\\bigplatform.png", -35, 1))
        self.platforms.add(Platform("img\\bigplatform.png", 415, 1))

        self.platforms.add(Platform("img\\leftwall.png", 0, 20))
        self.platforms.add(Platform("img\\leftwall.png", 0, 111))

        self.platforms.add(Platform("img\\rightwall.png", 680, 20))
        self.platforms.add(Platform("img\\rightwall.png", 680, 111))


    """
    В этой функции проверям события, проверяем не закрыл ли игрок окно
    """
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == SPAWN_ENEMY:
                if self.enemy_counter % 10 == 0:
                    pg.time.set_timer(SPAWN_ENEMY, 0)
                    self.enemy_spawn_time -= 500
                    pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
                self.enemies.add(Enemy())
                self.enemy_counter += 1
            if event.type == SHOT_FIRED:
                self.on_shot_fired()


    """
    Закрашиваем экран цветом фона
    """
    def fill(self):
        self.canvas.blit(self.bg_image,(0,0))

    """
    Отрисовываем положение объектов заново
    """
    def draw(self):
        self.player.draw(self.canvas)
        self.player.weapon.draw(self.canvas)
        self.platforms.draw(self.canvas)
        self.enemies.draw(self.canvas)
        self.bullets.draw(self.canvas)
        self.crates.draw(self.canvas)
        self.draw_text(str(self.score), 22, BLACK, WIDTH/2, 14)
        self.draw_text(str(self.player.weapon.name), 22, BLACK,100,100)
        pg.display.flip()


    def check_collision(self):
        for crate in self.crates:
            if pg.sprite.collide_rect(self.player, crate):
                self.score +=1
                self.player.weapon = random.choice(self.weapons)
                crate.kill()
                self.crates.add(Crate(random.choice(self.crates_spawn_positions)))
        for platform in self.platforms:
            if pg.sprite.collide_rect(platform, self.player):
                if self.player.rect.bottom > platform.rect.top and\
                self.player.rect.top < platform.rect.top:
                    self.player.rect.bottom = platform.rect.top
                    self.player.vel_y = 0
                    self.player.can_jump = True
                elif  self.player.rect.bottom > platform.rect.bottom and\
                self.player.rect.top < platform.rect.bottom:
                    self.player.rect.top = platform.rect.bottom
                    self.player.vel_y = GRAVITY
                    self.player.can_jump = False

                elif self.player.rect.left < platform.rect.right and\
                self.player.rect.right > platform.rect.right:
                    self.player.rect.left = platform.rect.right
                elif self.player.rect.right > platform.rect.left and\
                self.player.rect.left < platform.rect.left:
                    self.player.rect.right = platform.rect.left

            for enemy in self.enemies:
                if pg.sprite.collide_rect(enemy, self.player):
                    self.playing = False
                if pg.sprite.collide_rect(platform, enemy):
                    if enemy.rect.bottom > platform.rect.top and\
                    enemy.rect.top < platform.rect.top:
                        enemy.rect.bottom = platform.rect.top
                        enemy.vel_y = 0
                        enemy.can_jump = True
                    elif  enemy.rect.bottom > platform.rect.bottom and\
                    enemy.rect.top < platform.rect.bottom:
                        enemy.rect.top = platform.rect.bottom
                        enemy.vel_y = GRAVITY
                        enemy.can_jump = False

                    elif enemy.rect.left < platform.rect.right and\
                    enemy.rect.right > platform.rect.right:
                        enemy.rect.left = platform.rect.right
                        enemy.direction = - enemy.direction
                    elif enemy.rect.right > platform.rect.left and\
                    enemy.rect.left < platform.rect.left:
                        enemy.rect.right = platform.rect.left
                        enemy.direction = - enemy.direction

                for bullet in self.bullets:
                    if pg.sprite.collide_rect(bullet, platform):
                        bullet.kill()
                    if pg.sprite.collide_rect(enemy, bullet):
                        enemy.hp -= bullet.damage
                        bullet.kill()
                        if enemy.hp <= 0:
                            enemy.kill()
                        if bullet.dir_x > WIDTH or bullet.dir_x < 0:
                            print(bullet.dir_x)
                            bullet.kill()
                        if bullet.dir_y > HEIGHT or bullet.dir_y < 0:
                            bullet.kill()


    """
    Вспомогательная функция для отрисовки текста
    """
    def draw_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

    def on_shot_fired(self):
        self.bullets.add(Bullet(self.player.rect.centerx,self.player.rect.centery, self.player.direction,0 ,self.player.weapon))

game = Game()
while game.running:
    game.new()

pg.quit()
