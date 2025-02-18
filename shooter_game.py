from random import randint
from pygame import *
window = display.set_mode((1000,700))
display.set_caption('Шутер')
bg = transform.scale(image.load('galaxy.jpg'), (1000, 700))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 48) 
font2 = font.SysFont('Arial', 96) 

class GameSprite(sprite.Sprite):
    def __init__(self, image1, x_cord, y_cord, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image1), (size_x, size_y))
        self.speed = speed 
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 930:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 13, self.rect.top, 25, 50, 20)
        Bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y >= 600:
            lost += 1
            self.rect.x = randint(50, 850)
            self.rect.y = -(100)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
            




lost = 0
score = 0
Bullets = sprite.Group()
Enemies = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(50, 950 - 100), -100, 150, 100, randint(1,10))
    Enemies.add(monster)
Player = Player('rocket.png', 0, 550, 70, 150, 20)
Finish = False
Game = True
while Game != False:
    for e in event.get():
        if e.type == QUIT:
            Game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                Player.fire()
    if Finish == False:
        window.blit(bg, (0, 0))
        text = font1.render(f"Счет: {score}", 1, (255, 255, 255))
        window.blit(text, (5, 20))
        text2 = font1.render(f"Пропущено: {lost}", 1, (255,255,255))
        window.blit(text2, (5, 66))
        Player.reset()
        Player.update()
        Enemies.draw(window)
        Enemies.update()
        Bullets.update()
        Bullets.draw(window)
        

        monster_bullet = sprite.groupcollide(Enemies, Bullets, True, True)
        for i in monster_bullet:
            score += 1
            monster = Enemy('ufo.png', randint(50, 950 - 100), -100, 150, 100, randint(1,10))
            Enemies.add(monster)
        

        if sprite.spritecollide(Player, Enemies, False) or lost >= 3:
            Finish = True
            lose = font2.render(f"Вы проиграли!", 1, (255, 0, 0))
            window.blit(lose, (250, 300))
        elif score == 10:
            Finish = True
            win = font2.render(f"Вы выиграли!", 1, (0, 255, 0))
            window.blit(win, (250, 300))
        display.update()
    else:
        Finish = False
        score = 0
        lost = 0
        for b in Bullets:
            b.kill()
        for s in Enemies:
            s.kill()
        time.delay(2000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(50, 950 - 100), -100, 150, 100, randint(1,10))
            Enemies.add(monster)
    time.delay(50)    