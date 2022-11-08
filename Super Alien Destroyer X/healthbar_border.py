import pygame
import os
from healthbar import HealthBar
from lives import Lives

class HealthBorder(pygame.sprite.Sprite):
    def __init__(self,hp,num_lives):
        super(HealthBorder,self).__init__()
        self.image = pygame.image.load(os.path.join('Assets','Healthbar_border.png'))
        self.image = pygame.transform.scale(self.image,(400,30))
        self.rect = self.image.get_rect()
        self.rect.y = 720 - 20 - 20
        self.rect.x = 100
        self.healthBar = HealthBar(hp)
        self.lives = Lives(num_lives)
        self.healthBar_group = pygame.sprite.Group()
        self.healthBar_group.add(self.healthBar)
        self.healthBar_group.add(self.lives)

        