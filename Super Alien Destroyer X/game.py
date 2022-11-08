import pygame
import os
import time
from states.title import Title

class Game():
    def __init__(self):
        pygame.init()

        #Volume Setup
        pygame.mixer.Channel(0).set_volume(.1)
        pygame.mixer.Channel(1).set_volume(.1)
        pygame.mixer.Channel(2).set_volume(.1)
        pygame.mixer.Channel(3).set_volume(.1)
        pygame.mixer.Channel(4).set_volume(.1)
        pygame.mixer.Channel(5).set_volume(.1)
        pygame.mixer.Channel(6).set_volume(.1)

        #Display Setup
        self.FPS = 60
        self.width = 1280
        self.height = 720
        self.game_canvas = pygame.Surface((self.width,self.height))
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Super Alien Destroyer X')

        self.running = True
        self.playing = True

        self.delta_time = 0
        self.previous_time = 0

        self.state_stack = []

        self.load_assets()
        self.load_states()

        self.actions = {'escape': False, 'e': False}

    def game_loop(self):
        self.clock = pygame.time.Clock()
        while self.playing:
            self.clock.tick(self.FPS) 
            self.get_delta_time()
            self.get_events()
            self.update()
            self.render()
            #print(len(self.state_stack))
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = True
                if event.key == pygame.K_e:
                    self.actions['e'] = True
    
    def update(self):
        self.state_stack[-1].update(self.delta_time,self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)

        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.width,self.height)),(0,0))
        pygame.display.flip()
        pygame.display.update()

    def get_delta_time(self):
        now = time.time()
        self.delta_time = now - self.previous_time
        self.previous_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        self.font = pygame.font.SysFont('arial',16)
    
    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
