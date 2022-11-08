import pygame
import os 

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.width,self.height = 20,20
        self.image = pygame.image.load(os.path.join('Assets', 'bullet_.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.sound = pygame.mixer.Sound(os.path.join('Assets','laser.mp3'))
        self.rect = self.image.get_rect()
        self.speed = 30
    def update(self):
        self.rect.y -= self.speed

