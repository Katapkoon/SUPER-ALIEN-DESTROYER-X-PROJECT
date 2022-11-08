import pygame
import os
import random
from enemy_bullet import EnemyBullet
from explosion import Explosion

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.is_destroyed = False
        self.destroyed_sound = pygame.mixer.Sound(os.path.join('Assets','Explosion.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.wav'))
        self.image = pygame.image.load(os.path.join('Assets','enemy1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,1280 - 100)
        self.rect.y = -100
        self.vel_y = random.randrange(2,4)
        self.vel_x = 0
        self.hp = 2
        
        self.explosion_group = pygame.sprite.Group()
        

        self.states = {'fly_down' : 'fly_down', 'attack': 'attack'}
        self.current_state = self.states['fly_down']
        self.init_state = True

        self.bullets = pygame.sprite.Group()
        self.bullet_timer_max = 100
        self.bullet_timer = self.bullet_timer_max

        self.is_alive = True

        self.alpha = 0

        self.kill_time = 0

        self.timer = 500
        self.attacking_timer_max = 600
        self.attacking_timer = self.attacking_timer_max

        self.from_start = True

    def update(self):
        self.bullets.update()
        if self.current_state == 'fly_down':
            self.state_fly_down()
        elif self.current_state == 'attack':
            self.state_attack()
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.is_destroyed:
            explosion = Explosion(self.rect.x,self.rect.y)
            self.explosion_group.add(explosion)
            self.is_destroyed = False
            self.is_alive = False

        if not self.is_alive:
            self.image.set_alpha(self.alpha)
            self.timer -= 1
        
        if self.timer <= 0:
            self.kill()

    def get_hit(self):
        self.hp -= 1
        pygame.mixer.Channel(2).play(self.hit_sound)
        if self.hp <= 0:
            pygame.mixer.Channel(1).play(self.destroyed_sound)
            self.is_destroyed = True
        else:
            self.image = pygame.image.load(os.path.join('Assets','enemy_hit.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image,(70,70))

    def state_fly_down(self):
        rand = [100,150,200,250,300,350,400]
        if self.init_state:
            self.init_state = False
        if self.rect.y >= random.choice(rand) and self.from_start:
            self.current_state = self.states['attack']
            self.init_state = True
            self.from_start = False
        

    def state_attack(self):
        rand = random.randrange(0,100)
        self.attacking_timer -= 1
        if self.init_state:
            self.vel_y = 0
            while self.vel_x == 0:
                self.vel_x = random.randrange(-4,4)
            self.init_state = False
        
        if self.bullet_timer == 0 and self.is_alive:
            self.shoot()
            self.bullet_timer =self.bullet_timer_max
        else:
            self.bullet_timer -= 1

        if self.rect.x <= 0:
            self.vel_x *= -1
        elif self.rect.x >= 1280 - 80:
            self.vel_x *= -1
        
        if self.attacking_timer <= 0 and not self.from_start and rand < 50:
            self.vel_x = 0
            self.vel_y = random.randrange(2,4)
            self.current_state = self.states['fly_down']
            self.init_state = True
            self.attacking_timer = self.attacking_timer_max

    def shoot(self):
        new_bullet = EnemyBullet()
        new_bullet.speed *= -1
        new_bullet.rect.x = self.rect.x + 80//2 - new_bullet.width//2
        new_bullet.rect.y = self.rect.y + 80
        self.bullets.add(new_bullet)
        pygame.mixer.Channel(4).play(new_bullet.sound)


