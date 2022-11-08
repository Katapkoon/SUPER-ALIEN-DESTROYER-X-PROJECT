import pygame
import os


class HealthBar(pygame.sprite.Sprite):
    def __init__(self,hp):
        super(HealthBar,self).__init__()
        self.max_hp = hp
        self.hp = self.max_hp
        self.original_image = pygame.image.load(os.path.join('Assets','Bar1.png'))
        self.image = self.original_image
        self.image = pygame.transform.scale(self.image,(400,30))
        self.max_width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 720 - 20 - 20
        self.font = pygame.font.SysFont('arial', 20)
        self.text = self.font.render(str(self.hp), True, (255,255,255))
    
    def decrease_hp(self,hp):
        self.hp -= hp
        if self.hp < 0:
            self.hp = 0
        self.image = pygame.transform.scale(self.original_image,((self.max_width * self.hp)//self.max_hp,30))

    def reset_hp(self):
        self.hp = self.max_hp
        self.image = pygame.transform.scale(self.original_image,((self.max_width * self.hp)//self.max_hp,30))
    
    def update_hp(self):
        self.text = self.font.render(str(self.hp), True, (255,255,255))