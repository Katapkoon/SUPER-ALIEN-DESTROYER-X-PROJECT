import pygame
import os
from bullet import Bullet
from healthbar_border import HealthBorder

class Player(pygame.sprite.Sprite):
    def __init__(self,width,length):
        super(Player, self).__init__()
        self.width = width
        self.length = length
        self.image = pygame.image.load(os.path.join('Assets', 'ship.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.width,self.length))
        self.rect = self.image.get_rect()
        self.rect.x = 1280 // 2 - 100
        self.rect.y = 720 // 2 + 200
        self.bullets = pygame.sprite.Group()
        self.speed = 15
        self.hp = 4000
        self.lives = 5
        self.vulnerable_sound = pygame.mixer.Sound(os.path.join('Assets','damaged.wav'))
        self.health_border = HealthBorder(self.hp,self.lives)
        self.health_border_group = pygame.sprite.Group()
        self.health_border_group.add(self.health_border)
        self.flying = False
        self.prev_posx = 1280 // 2 - 100
        self.prev_posy = 720 // 2 + 200
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.wav'))
    
    def update(self):
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                self.bullets.remove(bullet)
        
    def shoot(self):
        new_bullet = Bullet()
        new_bullet.rect.x = self.rect.x + self.width//2 - new_bullet.width//2
        new_bullet.rect.y = self.rect.y
        self.bullets.add(new_bullet)
        pygame.mixer.Channel(0).play(new_bullet.sound)
    
    def get_hit(self,hp):
        if self.health_border.healthBar.hp > 0:
            self.health_border.healthBar.decrease_hp(hp)
        if self.health_border.healthBar.hp <= 0:
            self.health_border.healthBar.hp = 0
        if self.health_border.healthBar.hp == 0:
            self.death()
        

    def death(self):
        self.health_border.healthBar.reset_hp()
        self.lives -= 1
        if self.health_border.lives.num_lives <= 0:
            self.health_border.lives.num_lives = 0
        self.health_border.lives.decrement_life()

        #Reset Position (Optional : Add invicibility timer after death)
        self.rect.x = 1280 // 2 - 100
        self.rect.y = 720 // 2 + 200
    
    def move_check(self):
        self.prev_posx = self.rect.x
        self.prev_posy = self.rect.y 