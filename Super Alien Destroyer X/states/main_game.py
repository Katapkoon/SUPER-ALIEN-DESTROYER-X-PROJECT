import pygame, os
import math
from states.state import State
from star_animation import Background
from player import Player
from score import Score
from enemy_spawner import EnemySpawner
from enemy import Enemy
from enemy2 import Golem
from enemy3 import SideEnemy
from states.pause_menu import PauseMenu

class MainGame(State):
    def __init__(self,game):
        State.__init__(self,game)

        #Initialize Timer
        self.current_time = 0
        self.damaged_time = 0
        self.damaged_time_bullet = 0

        #In-Game Music setup
        pygame.mixer.music.load(os.path.join('BGM','Stargunner.mp3'))
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)

        #Initialize Background Elements
        self.background_image = pygame.image.load(os.path.join('Assets','background_2.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background_image,(1280,720))
        self.stars_anim = Background()
        self.star_imgs_group = pygame.sprite.Group()
        self.star_imgs_group.add(self.stars_anim)

        #Initialize Player Elements
        self.player = Player(70,70)
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player)
        self.canAttack = True
        self.vulnerable = False
        self.moving = False 
        self.score = Score()
        self.score_group = pygame.sprite.Group()
        self.score_group.add(self.score)
        self.ship_jet_width,self.ship_jet_height = 15,75
        self.ship_jet_image = pygame.image.load(os.path.join('Assets', 'jet.png')).convert_alpha()
        self.ship_jet = pygame.transform.scale(self.ship_jet_image,(self.ship_jet_width,self.ship_jet_height))

        self.hp_text_image = pygame.image.load(os.path.join('Assets','hp_text.png')).convert_alpha()
        self.hp_text = pygame.transform.scale(self.hp_text_image,(50,25))

        #Initialize shooting cooldown
        self.current_shooting_cooldown = 0
        self.shooting_cooldown_amount = 10

        #Initialize Enemy Spawner
        self.enemy_spawner = EnemySpawner()

        self.enemy_bullets = pygame.sprite.Group()
    
    def wave_value(self):
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self,delta_time,actions):
        #Get ticks when the game starts
        self.current_time = pygame.time.get_ticks()

        #Check player movement
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] and self.player.rect.y > 0:
            self.player.rect.y -= self.player.speed
        if key_pressed[pygame.K_s] and self.player.rect.y < 720-100:
            self.player.rect.y += self.player.speed
        if key_pressed[pygame.K_a] and self.player.rect.x > 0:
            self.player.rect.x -= self.player.speed
        if key_pressed[pygame.K_d] and self.player.rect.x < 1280-100:
            self.player.rect.x += self.player.speed
        if key_pressed[pygame.K_SPACE] and self.current_shooting_cooldown == 0 and self.canAttack:
            self.player.shoot()
            self.current_shooting_cooldown = 1
            #print('Shoot')
        if actions['escape'] == True:
            pygame.mixer.music.pause()
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        if actions['e'] == True:
            #for enemy in self.enemy_spawner.enemy_group:
                #enemy.kill()
            pass

        if self.player.prev_posx - self.player.rect.x == 0 and self.player.prev_posy - self.player.rect.y == 0:
            self.moving = False
        else:
            self.moving = True
            
        #Cooldown handle
        if self.current_shooting_cooldown >= self.shooting_cooldown_amount:
            self.current_shooting_cooldown = 0
        elif self.current_shooting_cooldown > 0:
            self.current_shooting_cooldown += 1

        #Update objects
        self.star_imgs_group.update()
        self.sprite_group.update()
        self.enemy_spawner.update()
        self.player.bullets.update()
        self.score_group.update()
        for enemy in self.enemy_spawner.enemy_group:
            enemy.explosion_group.update()

        #Check collision
        for enemy in self.enemy_spawner.enemy_group:
            for bullet in self.player.bullets:
                if pygame.sprite.collide_rect(bullet,enemy) and enemy.is_alive:
                    enemy.get_hit()
                    bullet.kill()

        for enemy in self.enemy_spawner.enemy_group:
            if pygame.sprite.collide_rect(enemy,self.player) and enemy.is_alive and not self.vulnerable:
                self.damaged_time = pygame.time.get_ticks()
                enemy.get_hit()
                self.vulnerable = True
                if type(enemy) is Enemy:
                    self.player.get_hit(1000)
                elif type(enemy) is SideEnemy:
                    self.player.get_hit(2000)
                elif type(enemy) is Golem:
                    self.player.get_hit(3000)
                pygame.mixer.Channel(3).play(self.player.vulnerable_sound)
        
        for enemy in  self.enemy_spawner.enemy_group:
            for bullet in enemy.bullets:
                if pygame.sprite.collide_rect(bullet,self.player) and not self.vulnerable:
                    self.damaged_time = pygame.time.get_ticks()
                    self.player.get_hit(500)
                    self.vulnerable = True
                    pygame.mixer.Channel(3).play(self.player.vulnerable_sound)
                    pygame.mixer.Channel(5).play(self.player.hit_sound)
                    bullet.kill()

        for enemy in self.enemy_spawner.enemy_group:
            if type(enemy) is Golem:
                if enemy.rect.y == 720:
                    self.player.health_border.lives.decrement_life()
        
        if self.vulnerable:
            alpha = self.wave_value()
            self.player.image.set_alpha(alpha)
        #Reset Player Debuffs
        if self.current_time - self.damaged_time > 2000:
            self.vulnerable = False
            self.player.image = pygame.image.load(os.path.join('Assets', 'ship.png')).convert_alpha()
            self.player.image = pygame.transform.scale(self.player.image,(self.player.width,self.player.length))
        
        

        #Check player's position
        self.player.move_check()

        #Update player's hp
        self.player.health_border.healthBar.update_hp()

        self.game.reset_keys()
        print('Current time {}'.format(self.current_time) + ' ' + 'Damaged time {}'.format(self.damaged_time) + ' ' + 'Damaged time 2 {}'.format(self.damaged_time_bullet) )

    def render(self, display):
        display.fill((0,0,0))
        display.blit(self.background, (0,0))
        display.blit(self.score.text,(self.score.x,self.score.y))
        self.star_imgs_group.draw(display)
        self.sprite_group.draw(display)
        self.enemy_spawner.enemy_group.draw(display)
        for enemy in self.enemy_spawner.enemy_group:
            enemy.bullets.draw(display)
            enemy.explosion_group.draw(display)
        self.player.bullets.draw(display)
        if self.moving:  #Render blue flame when changing player's position
            display.blit(self.ship_jet,(self.player.rect.x + self.player.width/2 - self.ship_jet_width/2,self.player.rect.y + self.player.length - 10))
        #print(self.moving)

        display.blit(self.hp_text,(25,720-20-20))
        self.player.health_border.healthBar_group.draw(display)
        self.player.health_border_group.draw(display)
        display.blit(self.player.health_border.healthBar.text,(125,720-20-16))
        
        #print(self.player.health_border.healthBar.hp)
        