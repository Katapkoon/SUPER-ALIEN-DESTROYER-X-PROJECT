import pygame, os
import math
import random
from states.state import State
from star_animation import Background
from planet import Planet
from moon import Moon
from player import Player
from score import Score
from enemy_spawner import EnemySpawner
from enemy import Enemy
from enemy2 import Golem
from enemy3 import SideEnemy
from states.pause_menu import PauseMenu
from states.gameover import GameOver
from item_spawner import ItemSpawner
from items.bomb import Bomb
from items.heart import Heart
from items.missile import Missile
from items.widebullet_item import WideBulletItem
from bullet import Bullet
from missile_bullet import MissileBullet
from wide_bullet import WideBullet

class MainGame(State):
    def __init__(self,game):
        State.__init__(self,game)

        self.gameOver = False
        self.canPressButton = True
        self.game.text_input.set_text('')
        #Initialize Timer
        self.current_time = 0
        self.damaged_time = 0
        self.item_time = 0
        self.damaged_time_bullet = 0
        self.gameOver_timer = 100

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
        self.planet = Planet()
        self.planet_group = pygame.sprite.Group()
        self.planet_group.add(self.planet)
        self.moon = Moon()
        self.moon_group = pygame.sprite.Group()
        self.moon_group.add(self.moon)

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

        self.score_check = 50000

        #Initialize shooting cooldown
        self.current_shooting_cooldown = 0
        self.shooting_cooldown_amount = 10

        #Initialize Enemy Spawner
        self.enemy_spawner = EnemySpawner()

        self.enemy_bullets = pygame.sprite.Group()

        #Initialize item spawner
        self.item_spawner = ItemSpawner()
    
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
        if key_pressed[pygame.K_w] and self.player.rect.y > 0 and self.canPressButton:
            self.player.rect.y -= self.player.speed
        if key_pressed[pygame.K_s] and self.player.rect.y < 720-100 and self.canPressButton:
            self.player.rect.y += self.player.speed
        if key_pressed[pygame.K_a] and self.player.rect.x > 0 and self.canPressButton:
            self.player.rect.x -= self.player.speed
        if key_pressed[pygame.K_d] and self.player.rect.x < 1280-100 and self.canPressButton:
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
        self.planet_group.update()
        self.moon_group.update()
        self.sprite_group.update()
        self.enemy_spawner.update()
        self.player.bullets.update()
        self.score_group.update()
        for enemy in self.enemy_spawner.enemy_group:
            enemy.explosion_group.update()
        self.player.explosion_group.update()
        self.item_spawner.update()

        #Check collision
        for enemy in self.enemy_spawner.enemy_group:
            for bullet in self.player.bullets:
                if pygame.sprite.collide_rect(bullet,enemy) and enemy.is_alive:
                    if type(bullet) is Bullet:
                        enemy.get_hit(1)
                        bullet.kill()
                    if type(bullet) is MissileBullet:
                        enemy.get_hit(10)
                        bullet.kill()
                    if type(bullet) is WideBullet:
                        enemy.get_hit(10)

        for enemy in self.enemy_spawner.enemy_group:
            if pygame.sprite.collide_rect(enemy,self.player) and enemy.is_alive and not self.vulnerable and not self.player.is_destroyed:
                self.damaged_time = pygame.time.get_ticks()
                enemy.get_hit(1)
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
                if pygame.sprite.collide_rect(bullet,self.player) and not self.vulnerable and not self.player.is_destroyed:
                    self.damaged_time = pygame.time.get_ticks()
                    self.player.get_hit(500)
                    self.vulnerable = True
                    pygame.mixer.Channel(3).play(self.player.vulnerable_sound)
                    pygame.mixer.Channel(5).play(self.player.hit_sound)
                    bullet.kill()

        for enemy in self.enemy_spawner.enemy_group:
            if type(enemy) is Golem:
                if enemy.rect.y == 720 and enemy.is_alive:
                    self.player.health_border.lives.decrement_life()
            
            if enemy.is_destroyed:
                if type(enemy) is Enemy:
                    self.item_spawner.spawn_item(enemy.rect.x + 35,enemy.rect.y + 35)
                    self.score.score_num += 500 + (self.player.rect.y - enemy.rect.y)
                elif type(enemy) is Golem:
                    self.item_spawner.spawn_item(enemy.rect.x + 50,enemy.rect.y + 50)
                    self.score.score_num += 750 + (self.player.rect.y - enemy.rect.y)
                elif type(enemy) is SideEnemy:
                    self.item_spawner.spawn_item(enemy.rect.x + 50,enemy.rect.y + 25)
                    self.score.score_num += 1000 + (self.player.rect.y - enemy.rect.y)
        
        for item in self.item_spawner.item_group:
            if pygame.sprite.collide_rect(item, self.player):
                if type(item) is Bomb:
                    self.score.score_num += 200
                    item.kill()
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join('Assets', 'collect.mp3')))
                    for enemy in self.enemy_spawner.enemy_group:
                        if enemy.is_alive:
                            enemy.get_hit(10)
                if type(item) is Heart:
                    self.player.health_border.healthBar.reset_hp()
                    self.score.score_num += 200
                    self.player.health_border.lives.increment_life()
                    item.kill()
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join('Assets', 'collect.mp3')))
                if type(item) is Missile:
                    self.score.score_num += 200
                    self.item_spawner.can_spawnItem = False
                    self.item_time = pygame.time.get_ticks()
                    self.shooting_cooldown_amount = 12
                    item.kill()
                    self.player.current_state = self.player.states['missile']
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join('Assets', 'collect.mp3')))
                if type(item) is WideBulletItem:
                    self.item_time = pygame.time.get_ticks()
                    self.score.score_num += 200
                    self.item_spawner.can_spawnItem = False
                    item.kill()
                    self.player.current_state = self.player.states['wide bullet']
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join('Assets', 'collect.mp3')))

        if self.vulnerable:
            alpha = self.wave_value()
            self.player.image.set_alpha(alpha)
        #Reset Player Debuffs
        if self.current_time - self.damaged_time > 2000:
            self.vulnerable = False
            self.player.image = pygame.image.load(os.path.join('Assets', 'ship.png')).convert_alpha()
            self.player.image = pygame.transform.scale(self.player.image,(self.player.width,self.player.length))
        
        #Reset Player Buffs
        if self.current_time - self.item_time > 10000:
            self.item_spawner.can_spawnItem = True
            self.player.current_state = self.player.states['normal']
            self.shooting_cooldown_amount = 10

        #Check player's position
        self.player.move_check()

        #Update player's hp
        self.player.health_border.healthBar.update_hp()

        self.game.reset_keys()
        #print('Current time {}'.format(self.current_time) + ' ' + 'Damaged time {}'.format(self.damaged_time) + ' ' + 'Damaged time 2 {}'.format(self.damaged_time_bullet) )
        
        #print(self.gameOver_timer)

        if self.player.health_border.lives.num_lives <= 0:
            self.player.is_destroyed = True 
            self.vulnerable = False
            self.canAttack = False
            self.canPressButton = False
            self.gameOver = True    
        
        if self.gameOver:
            self.player.health_border.lives.kill()
            self.player.health_border.kill()
            self.player.health_border.healthBar.kill()
            self.player.image.set_alpha(0)
            self.gameOver_timer -= 1
        
        if self.gameOver_timer <= 0:
            self.player.kill()
            new_state = GameOver(self.game,self.score.score_num)
            new_state.enter_state()
            pygame.mixer.music.stop()

        if self.score.score_num > self.score_check:
            self.enemy_spawner.init_spawn_rate -= 2
            self.score_check += 50000
        
    def render(self, display):
        display.fill((0,0,0))
        display.blit(self.background, (0,0))
        display.blit(self.score.text,(self.score.x,self.score.y))
        self.star_imgs_group.draw(display)
        self.planet_group.draw(display)
        self.moon_group.draw(display)
        self.sprite_group.draw(display)
        self.enemy_spawner.enemy_group.draw(display)
        for enemy in self.enemy_spawner.enemy_group:
            enemy.bullets.draw(display)
            enemy.explosion_group.draw(display)
        self.player.bullets.draw(display)
        if self.moving:  #Render blue flame when changing player's position
            display.blit(self.ship_jet,(self.player.rect.x + self.player.width/2 - self.ship_jet_width/2,self.player.rect.y + self.player.length - 10))
        #print(self.moving)
        self.item_spawner.item_group.draw(display)

        self.player.explosion_group.draw(display)
        self.player.health_border.healthBar_group.draw(display)
        self.player.health_border_group.draw(display)
        if not self.gameOver:
            display.blit(self.hp_text,(25,720-20-20))
            display.blit(self.player.health_border.healthBar.text,(125,720-20-16))
    
        #print(self.player.health_border.healthBar.hp)
        #print(str(self.player.health_border.lives.num_lives) + ' ' + str(self.player.alpha))
        print(self.enemy_spawner.init_spawn_rate)