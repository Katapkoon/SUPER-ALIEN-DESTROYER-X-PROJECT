import pygame
import os

class WideBulletItem(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(WideBulletItem,self).__init__()
        self.image = pygame.image.load(os.path.join('Assets','wide_bullet.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(60,25))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel_y = 5
        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.y >= 720 + 40:
            self.kill()