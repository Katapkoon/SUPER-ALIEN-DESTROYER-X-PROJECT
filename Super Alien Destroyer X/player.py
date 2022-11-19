import pygame
import os
from bullet import Bullet
from missile_bullet import MissileBullet
from wide_bullet import WideBullet
from healthbar_border import HealthBorder
from explosion import Explosion

class Player(pygame.sprite.Sprite):
    def __init__(self,width,length):
        super(Player, self).__init__()
        self.isGameOver = False
        self.width = width
        self.length = length
        self.alpha = 255
        self.image = pygame.image.load(os.path.join('Assets', 'ship.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.width,self.length))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.x = 1280 // 2 - 100
        self.rect.y = 720 // 2 + 200
        self.bullets = pygame.sprite.Group()
        self.speed = 15
        self.hp = 4000
        self.lives = 1
        self.vulnerable_sound = pygame.mixer.Sound(os.path.join('Assets','damaged.wav'))
        self.health_border = HealthBorder(self.hp,self.lives)
        self.health_border_group = pygame.sprite.Group()
        self.health_border_group.add(self.health_border)
        self.flying = False
        self.prev_posx = 1280 // 2 - 100
        self.prev_posy = 720 // 2 + 200
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.wav'))
        self.is_destroyed = False
        self.is_alive = True
        self.explosion_group = pygame.sprite.Group()
        self.destroyed_sound = pygame.mixer.Sound(os.path.join('Assets','Explosion.wav'))
        self.isGameOver = False

        self.states = {'normal' : 'NORMAL','missile' : 'MISSILE', 'wide bullet' : 'WIDE_BULLET'}
        self.current_state = self.states['normal']
        self.init_state = True

    def update(self):

        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                self.bullets.remove(bullet)

        if self.health_border.lives.num_lives == 0:
            self.isGameOver = True
        else:
            self.isGameOver = False
        if self.isGameOver:
            self.gameOver()

    def shoot(self):
        if self.current_state == 'NORMAL':
            new_bullet = Bullet()
            new_bullet.rect.x = self.rect.x + self.width//2 - new_bullet.width//2
            new_bullet.rect.y = self.rect.y
            self.bullets.add(new_bullet)
            pygame.mixer.Channel(0).play(new_bullet.sound)
        if self.current_state == 'MISSILE':
            new_bullet = MissileBullet()
            new_bullet.rect.x = self.rect.x + self.width//2 - new_bullet.width//2
            new_bullet.rect.y = self.rect.y
            self.bullets.add(new_bullet)
            pygame.mixer.Channel(0).play(new_bullet.sound)
        if self.current_state == 'WIDE_BULLET':
            new_bullet = WideBullet()
            new_bullet.rect.x = self.rect.x + self.width//2 - new_bullet.width//2
            new_bullet.rect.y = self.rect.y
            pygame.mixer.Channel(0).play(new_bullet.sound)
            self.bullets.add(new_bullet)

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
            pass
        self.health_border.lives.decrement_life()

        #Reset Position (Optional : Add invicibility timer after death)
        if self.health_border.lives.num_lives > 0 :
            self.rect.x = 1280 // 2 - 100
            self.rect.y = 720 // 2 + 200
    
    def move_check(self):
        self.prev_posx = self.rect.x
        self.prev_posy = self.rect.y 
    
    def gameOver(self):
        self.health_border.lives.decrement_life()
        explosion = Explosion(self.rect.x,self.rect.y)
        self.explosion_group.add(explosion)
        pygame.mixer.Channel(7).play(self.destroyed_sound)
        self.isGameOver = False
        pygame.mixer.music.stop()
        


