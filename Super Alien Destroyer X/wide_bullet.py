import pygame
import os

class WideBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(WideBullet,self).__init__()
        self.width,self.height = 120*1.5,50*1.5
        self.image = pygame.image.load(os.path.join('Assets', 'wide_bullet.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.sound = pygame.mixer.Sound(os.path.join('Assets','widebullet_shoot.wav'))
        self.rect = self.image.get_rect()
        self.speed = 30
        self.size_increase = 10

    def update(self):
        self.rect.y -= self.speed