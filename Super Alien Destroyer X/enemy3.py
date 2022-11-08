import pygame
import os
import random

from explosion import Explosion

class SideEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(SideEnemy,self).__init__()
        self.is_destroyed = False
        self.is_alive = True
        self.start_x = { '1' : 0, '2' : 1280}
        self.dir_x = 1
        self.rand_x = random.choice(list(self.start_x.values()))
        self.start_y = random.randrange(300,600)
        self.image = pygame.image.load(os.path.join('Assets','enemy3.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,50))
        self.rect = self.image.get_rect()
        self.rect.x = self.rand_x
        if self.rand_x == self.start_x['2']:
            self.dir_x = -1
        self.rect.y = self.start_y
        self.vel_x = 15
        self.vel_y = 0
        self.alpha = 0
        self.explosion_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.timer = 500
        self.hp = 3
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.wav'))
        self.destroyed_sound = pygame.mixer.Sound(os.path.join('Assets','Explosion.wav'))

    def update(self):
        self.rect.x += self.vel_x * self.dir_x
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
        pygame.mixer.Channel(6).play(self.hit_sound)
        if self.hp <= 0:
            pygame.mixer.Channel(1).play(self.destroyed_sound)
            self.is_destroyed = True

    def render(self,display):
        pass
        


