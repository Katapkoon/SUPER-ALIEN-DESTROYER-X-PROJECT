import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Explosion,self).__init__()
        self.img_ex1 = pygame.image.load(os.path.join('Assets','ex1.png')).convert_alpha()
        self.img_ex1 = pygame.transform.scale(self.img_ex1,(80,80))

        self.img_ex2 = pygame.image.load(os.path.join('Assets','ex2.png')).convert_alpha()
        self.img_ex2 = pygame.transform.scale(self.img_ex2,(80,80))

        self.img_ex3 = pygame.image.load(os.path.join('Assets','ex3.png')).convert_alpha()
        self.img_ex3 = pygame.transform.scale(self.img_ex3,(80,80))

        self.img_ex4 = pygame.image.load(os.path.join('Assets','ex4.png')).convert_alpha()
        self.img_ex4 = pygame.transform.scale(self.img_ex4,(80,80))

        self.img_ex5 = pygame.image.load(os.path.join('Assets','ex5.png')).convert_alpha()
        self.img_ex5 = pygame.transform.scale(self.img_ex5,(80,80))

        self.img_ex6 = pygame.image.load(os.path.join('Assets','ex6.png')).convert_alpha()
        self.img_ex6 = pygame.transform.scale(self.img_ex6,(80,80))

        self.img_ex7 = pygame.image.load(os.path.join('Assets','ex7.png')).convert_alpha()
        self.img_ex7 = pygame.transform.scale(self.img_ex7,(80,80))

        self.img_ex8 = pygame.image.load(os.path.join('Assets','ex8.png')).convert_alpha()
        self.img_ex8 = pygame.transform.scale(self.img_ex8,(80,80))

        self.anim_explosion = [self.img_ex1, self.img_ex2, self.img_ex3, self.img_ex4, self.img_ex5, self.img_ex6, self.img_ex7, self.img_ex8]
        self.anim_index = 0
        self.image = self.anim_explosion[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_index = len(self.anim_explosion) - 1

    def update(self):
        if self.anim_index > self.max_index:
            self.kill()
        else:
            self.image = self.anim_explosion[self.anim_index]
            self.anim_index += 1
