import pygame
import os
from states.state import State
from menu_button import Button

class AboutCreator(State):
    def __init__(self,game):
        self.game = game
        State.__init__(self,game)
        self.font = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentric rg.otf')), 24)
        self.font_2 = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentric rg.otf')), 36)
        self.text = self.font.render('This game is created by Katapat Koonthamstit 65010101',True ,(150,210,255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (1280//2, 720//2)
        self.return_title_text = self.font_2.render('Return to the titlescreen', True, (255,255,255))
        self.return_title_button = Button(1280/2,500, self.return_title_text)
    
    def update(self, delta_time, actions):
        pygame.display.update()
    
    def render(self, display):
        display.fill((0,0,0))
        display.blit(self.text,(self.text_rect.x,self.text_rect.y))
        if self.return_title_button.update(display):
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop(-1)
        
        