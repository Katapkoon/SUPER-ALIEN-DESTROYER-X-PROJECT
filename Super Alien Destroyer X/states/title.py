import sys
from states.state import State
from states.main_game import MainGame 
from states.about_creator import AboutCreator
from states.leaderboard import Leaderboard
from menu_button import Button
from star_animation import Background
from player import Player
import pygame
import os
import math

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

        #Initialize menu elements
        self.font_1 = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentricrg.otf')), 24)
        self.font_2 = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentricrg.otf')), 16)
        self.logo = self.font_1.render('Super Alien Destroyer X',True ,(0,255,0))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (300,200)
        self.start_button_image = pygame.image.load(os.path.join('Assets','Menu','start_button.png')).convert_alpha()
        self.start_button_image = pygame.transform.scale(self.start_button_image,(200,50))
        self.exit_button_image = pygame.image.load(os.path.join('Assets','Menu','exit_button.png')).convert_alpha()
        self.exit_button_image = pygame.transform.scale(self.exit_button_image,(200,50))
        self.about_text = self.font_2.render('About',True ,(0,255,0))
        self.leaderboard_text = self.font_2.render('Leaderboard',True ,(0,255,0))
        self.start_button = Button(300, 400, self.start_button_image)
        self.exit_button = Button(300, 600, self.exit_button_image)
        self.about_button = Button(900,650,self.about_text)
        self.leaderboard_button = Button(1100,650,self.leaderboard_text)
        #Menu Music setup
        pygame.mixer.music.load(os.path.join('BGM','Blue Eclipse.mp3'))
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)

        #Menu background
        self.background = Background()
        self.background_img_group = pygame.sprite.Group()
        self.background_img_group.add(self.background)

        #Initialize props
        self.ship = Player(150,150)
        self.ship.rect.x = 800
        self.ship.rect.y = 300
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.ship)
        self.ship_jet_image = pygame.image.load(os.path.join('Assets', 'jet.png')).convert_alpha()
        self.ship_jet = pygame.transform.scale(self.ship_jet_image,(30,150))

        self.ship_flying = False

        self.creator_name_image = pygame.image.load(os.path.join('Assets','name.png')).convert_alpha()
        self.creator_name =  pygame.transform.scale(self.creator_name_image,(500,30))

        self.color = 0
        self.ascending = True
    def wave_color(self):
        if self.ascending and self.color < 255:
            self.color += 1
        elif self.color == 255:
            self.ascending = False
        
        if not self.ascending:
            self.color -= 1
            if self.color == 0:
                self.ascending = True
    def update(self, delta_time, actions):
        self.wave_color()
        self.logo = self.font_1.render('Super Alien Destroyer X',True ,(self.color,255,self.color))

        if self.ship_flying:
            self.ship.rect.y -= self.ship.speed
        if self.ship.rect.y < -150-150:
            self.ship_flying = False
            self.ship.rect.y = 300
            new_state = MainGame(self.game)
            new_state.enter_state()
        
        self.background_img_group.update()
        self.sprite_group.update()

        self.game.reset_keys()
        
    def render(self, display):
        display.fill((0,0,0))
        display.blit(self.logo,(self.logo_rect.x,self.logo_rect.y))
        #self.game.draw_text(display, "Titlescreen", (0,0,0), self.game.width/2, self.game.height/2)
        if self.start_button.update(display):
            self.ship_flying = True
            
        if self.exit_button.update(display):
            pygame.mixer.music.stop()
            sys.exit()
        if self.about_button.update(display):
            new_state = AboutCreator(self.game)
            new_state.enter_state()
        if self.leaderboard_button.update(display):
            new_state = Leaderboard(self.game)
            new_state.enter_state()
        
        self.background_img_group.draw(display)
        self.sprite_group.draw(display)

        if self.ship_flying:
            display.blit(self.ship_jet,(self.ship.rect.x + self.ship.width/2 - 15 ,self.ship.rect.y + 125))

        #display.blit(self.creator_name,(1280-500,720-30))
        