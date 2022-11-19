import pygame
import pygame_gui
import os
from states.state import State
from menu_button import Button
import json

class GameOver(State):
    def __init__(self,game,score):
        self.game = game
        self.score = score
        self.score_dict = {}

        State.__init__(self,game)
        self.font = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentric rg.otf')), 36)
        self.game_over_text = self.font.render('Game Over',True ,(255,0,0))
        self.gameOver_rect = self.game_over_text.get_rect()
        self.score_text = self.font.render('Score : ' + str(self.score),True ,(255,255,255))
        self.score_rect = self.score_text.get_rect()
        self.gameOver_rect.center = (1280/2, 200)
        self.score_rect.center = (1280/2, 350)
        self.return_title_text = self.font.render('Return to the titlescreen', True, (255,255,255))
        self.return_title_button = Button(1280/2,500, self.return_title_text)
        self.saved_text = self.font.render('SAVED!', True, (0,255,0))
        self.saved_text_rect = self.game_over_text.get_rect()
        self.saved_text_rect.center = (1280/2 + 50, 200)

    def update(self,delta_time, actions):
        self.game.manager.update(self.game.ui_refresh_rate)
        
        pygame.display.update()

    def render(self,display):
        if not self.game.text_entered:
            display.fill((0,0,0))
            self.game.manager.draw_ui(display)
            display.blit(self.game_over_text, (self.gameOver_rect.x, self.gameOver_rect.y))
            display.blit(self.score_text, (self.score_rect.x,self.score_rect.y))

        else:
            
            self.score_dict[self.game.temp_text] = self.score
            display.fill((0,0,0))
            display.blit(self.saved_text,(self.saved_text_rect.x,self.saved_text_rect.y))
            if self.return_title_button.update(display):
                self.game.text_entered = False
                with open("leaderb.json",mode='r',encoding='utf8') as f:
                    feeds = json.load(f)
    
                with open("leaderb.json",mode='w',encoding='utf8') as file:
                    feeds[self.game.temp_text]  = self.score
                    json.dump(feeds,file)
                
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop(-1)
                pygame.mixer.music.load(os.path.join('BGM','Blue Eclipse.mp3'))
                pygame.mixer.music.set_volume(.1)
                pygame.mixer.music.play(-1)