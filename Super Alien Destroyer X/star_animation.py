import pygame
import os

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.images = []
        for num in range(0,2):
            img = pygame.image.load(os.path.join('Assets','Background','bg ({}).png'.format(num+1))).convert_alpha()
            img = pygame.transform.scale(img, (1280,720))
            self.images.append(img)
        self.anim_index = 0
        self.max_anim_index = len(self.images) - 1
        self.max_frame_duration = 1
        self.frame_duration = self.max_frame_duration
        self.image = self.images[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    
    def update(self):
        if self.frame_duration == 0:
            self.anim_index += 1
            if self.anim_index > self.max_anim_index:
                self.anim_index = 0
            self.image = self.images[self.anim_index]
            self.frame_duration = self.max_frame_duration
        self.frame_duration -= 1
