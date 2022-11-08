import pygame
import os
import random

class Golem(pygame.sprite.Sprite):
    def __init__(self):
        super(Golem,self).__init__()
        self.img_ex1 = pygame.image.load(os.path.join('Assets','ex1.png')).convert_alpha()
        self.img_ex1 = pygame.transform.scale(self.img_ex1,(100,100))

        self.img_ex2 = pygame.image.load(os.path.join('Assets','ex2.png')).convert_alpha()
        self.img_ex2 = pygame.transform.scale(self.img_ex2,(100,100))

        self.img_ex3 = pygame.image.load(os.path.join('Assets','ex3.png')).convert_alpha()
        self.img_ex3 = pygame.transform.scale(self.img_ex3,(100,100))

        self.img_ex4 = pygame.image.load(os.path.join('Assets','ex4.png')).convert_alpha()
        self.img_ex4 = pygame.transform.scale(self.img_ex4,(100,100))

        self.img_ex5 = pygame.image.load(os.path.join('Assets','ex5.png')).convert_alpha()
        self.img_ex5 = pygame.transform.scale(self.img_ex5,(100,100))

        self.img_ex6 = pygame.image.load(os.path.join('Assets','ex6.png')).convert_alpha()
        self.img_ex6 = pygame.transform.scale(self.img_ex6,(100,100))

        self.img_ex7 = pygame.image.load(os.path.join('Assets','ex7.png')).convert_alpha()
        self.img_ex7 = pygame.transform.scale(self.img_ex7,(100,100))

        self.img_ex8 = pygame.image.load(os.path.join('Assets','ex8.png')).convert_alpha()
        self.img_ex8 = pygame.transform.scale(self.img_ex8,(100,100))

        self.anim_explosion = [self.img_ex1, self.img_ex2, self.img_ex3, self.img_ex4, self.img_ex5, self.img_ex6, self.img_ex7, self.img_ex8]
        self.anim_index = 0

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

        self.timer = 100

    def update(self):
        self.rect.y += self.vel_y
        if self.is_destroyed:
            max_index = len(self.anim_explosion) - 1
        
            if self.anim_index > max_index:
                self.kill()
            else:
                self.image = self.anim_explosion[self.anim_index]
                self.anim_index += 1

    def get_hit(self):
        self.hp -= 1
        pygame.mixer.Channel(2).play(self.hit_sound)
        if self.hp <= 0:
            pygame.mixer.Channel(1).play(self.destroyed_sound)
            self.is_destroyed = True

    def render(self,display):
       pass