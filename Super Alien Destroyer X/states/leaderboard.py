import pygame
import os
import json
from states.state import State
from menu_button import Button

class Leaderboard(State):
    def __init__(self,game):
        State.__init__(self,game)
        self.font = pygame.font.Font((os.path.join('Assets','Fonts','ethnocentric rg.otf')), 24)
        self.font_2 = pygame.font.SysFont('arial', 24)
        self.return_title_text = self.font.render('Return to the titlescreen', True, (255,255,255))
        self.return_title_button = Button(1280/2, 700, self.return_title_text)
        self.leaderboard_text = self.font.render('Leaderboard', True, (0,255,0))
        self.lb_rect = self.leaderboard_text.get_rect()
        self.lb_rect.center = (1280/2, 100)
        self.texts = []


        with open('leaderb.json','r') as file:
            self.score_dict = json.load(file)
        self.new_list = list(sorted(self.score_dict.items(), key=lambda d: d[1], reverse=True))
        print(self.new_list[0][0] + ' : ' + str(self.new_list[0][1]))

        self.len = len(self.new_list)
        if self.len > 5:
            self.len = 5
        for num in range(0,self.len):
            text = self.font_2.render(f"{num + 1}. {self.new_list[num][0]} : {str(self.new_list[num][1])}" ,True ,(255,255,255))
            self.texts.append(text)
        
        self.text_rects = []
        for num in range(0,self.len):
            rect = self.texts[num].get_rect()
            self.text_rects.append(rect)

        for num in range(0,self.len):
            self.text_rects[num].center = (1280//2,100 + 100*(num+1))

    def update(self,delta_time, actions):
        pygame.display.update()

    def render(self,display):
        display.fill((0,0,0))
        display.blit(self.leaderboard_text,(self.lb_rect.x,self.lb_rect.y))
        for num in range(0,self.len):
            display.blit(self.texts[num],(self.text_rects[num].x,self.text_rects[num].y))
        if self.return_title_button.update(display):
             while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop(-1)