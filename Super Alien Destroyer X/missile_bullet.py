import pygame
import os

class MissileBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(MissileBullet,self).__init__  ()
        self.width,self.height = 40,40
        self.image = pygame.image.load(os.path.join('Assets', 'missile_item','missile 1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.sound = pygame.mixer.Sound(os.path.join('Assets','missile_shoot.wav'))
        self.rect = self.image.get_rect()
        self.speed = 30

    def update(self):
        self.rect.y -= self.speed