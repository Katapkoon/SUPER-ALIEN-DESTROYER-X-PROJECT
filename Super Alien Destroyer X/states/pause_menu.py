import pygame
import os
from states.state import State
from menu_button import Button

class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self,game)
        #Initialize Pause menu elements
        self.font = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentric rg.otf')), 36)
        self.resume_text = self.font.render('Resume', True, (255,255,255))
        self.return_title_text = self.font.render('Return to the titlescreen', True, (255,255,255))
        self.resume_button = Button(1280/2, 300, self.resume_text)
        self.return_title_button = Button(1280/2,500, self.return_title_text)
        self.exit = False
    def update(self, delta_time,actions):
        if actions['escape']:
            pygame.mixer.music.unpause()
            self.exit_state()
        self.game.reset_keys()

    def render(self,display):
        display.fill((0,0,0))

        if self.resume_button.update(display):
            pygame.mixer.music.unpause()
            self.exit_state()
        
        if self.return_title_button.update(display):
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop(-1)
                pygame.mixer.music.load(os.path.join('BGM','Blue Eclipse.mp3'))
                pygame.mixer.music.set_volume(.1)
                pygame.mixer.music.play(-1)
            