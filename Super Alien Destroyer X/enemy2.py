import pygame
import os
import random
from explosion import Explosion

class Golem(pygame.sprite.Sprite):
    def __init__(self):
        super(Golem,self).__init__()
        self.is_destroyed = False
        self.destroyed_sound = pygame.mixer.Sound(os.path.join('Assets','Explosion.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.wav'))
        self.image = pygame.image.load(os.path.join('Assets','enemy2.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,1280 - 100)
        self.rect.y = -100
        self.vel_y = random.randrange(1,2)
        self.hp = 4
        
        self.bullets = pygame.sprite.Group()
        
        self.explosion_group = pygame.sprite.Group()

        self.is_alive = True

        self.timer = 500
        self.alpha = 0

    def update(self):
        self.rect.y += self.vel_y
        if self.is_destroyed:
            explosion = Explosion(self.rect.x + 50 - 40,self.rect.y + 50 - 40)
            self.explosion_group.add(explosion)
            self.is_destroyed = False
            self.is_alive = False
        
        if not self.is_alive:
            self.image.set_alpha(self.alpha)
            self.timer -= 1

        if self.timer <= 0:
            self.kill()

    def get_hit(self,hp):
        self.hp -= hp
        pygame.mixer.Channel(2).play(self.hit_sound)
        if self.hp <= 0:
            pygame.mixer.Channel(1).play(self.destroyed_sound)
            self.is_destroyed = True

    def render(self,display):
       pass