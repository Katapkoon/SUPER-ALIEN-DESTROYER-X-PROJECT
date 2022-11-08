import pygame
import os

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super(Planet, self).__init__()
        self.images = []
        for num in range(0,120):
            img = pygame.image.load(os.path.join('Assets','World','{}.png'.format(num+1))).convert_alpha()
            img = pygame.transform.scale(img, (200,200))
            self.images.append(img)
        self.anim_index = 0
        self.max_anim_index = len(self.images) - 1
        self.max_frame_duration = 5
        self.frame_duration = self.max_frame_duration
        self.image = self.images[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 400
    
    def update(self):
        if self.frame_duration == 0:
            self.anim_index += 1
            if self.anim_index > self.max_anim_index:
                self.anim_index = 0
            self.image = self.images[self.anim_index]
            self.frame_duration = self.max_frame_duration
        self.frame_duration -= 1
