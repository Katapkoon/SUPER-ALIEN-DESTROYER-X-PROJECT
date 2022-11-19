import os
import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Bomb, self).__init__()
        self.images = []
        for num in range(0,4):
            img = pygame.image.load(os.path.join('Assets','bomb_item','bomb ({}).png'.format(num + 1))).convert_alpha()
            img = pygame.transform.scale(img, (80,80))
            self.images.append(img)
        self.anim_index = 0
        self.max_anim_index = len(self.images) - 1
        self.max_frame_duration = 5
        self.frame_duration = self.max_frame_duration
        self.image = self.images[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel_y = 5
        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.y >= 720 + 40:
            self.kill()
        
        if self.frame_duration == 0:
            self.anim_index += 1
            if self.anim_index > self.max_anim_index:
                self.anim_index = 0
            self.image = self.images[self.anim_index]
            self.frame_duration = self.max_frame_duration
        self.frame_duration -= 1