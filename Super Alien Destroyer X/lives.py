import pygame
import os

class Lives(pygame.sprite.Sprite):
    def __init__(self, num_lives):
        super(Lives,self).__init__()
        self.num_lives = num_lives
        self.width = 110
        self.height = 40
        self.size = (self.width,self.height)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
        self.heart_image = pygame.image.load(os.path.join('Assets','Heart','Cuore1.png'))
        self.heart_image = pygame.transform.scale(self.heart_image,(self.heart_image.get_width()*2,self.heart_image.get_height()*2))
        self.image.blit(self.heart_image,(10,0))
        self.font = pygame.font.SysFont('arial', 24)
        self.lives_counter = self.font.render(f'x {self.num_lives}',False,(255,255,255))
        self.image.blit(self.lives_counter, (60,0))
        self.rect = self.image.get_rect()
    
    def decrement_life(self):
        self.num_lives -= 1
        if self.num_lives <= 0:
            pass
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
        self.image.blit(self.heart_image,(10,0))
        self.lives_counter = self.font.render(f'x {self.num_lives}',False,(255,255,255))
        self.image.blit(self.lives_counter, (60,0))

    def increment_life(self):
        self.num_lives += 1
        if self.num_lives >= 3:
            self.num_lives = 3
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
        self.image.blit(self.heart_image,(10,0))
        self.lives_counter = self.font.render(f'x {self.num_lives}',False,(255,255,255))
        self.image.blit(self.lives_counter, (60,0))

