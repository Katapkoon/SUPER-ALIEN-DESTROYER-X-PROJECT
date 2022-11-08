import pygame 
import os

class Button():
    def __init__(self,x,y,image):  
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
    
    def update(self,screen):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #Draw the button
        screen.blit(self.image,(self.rect.x, self.rect.y))

        return action

        
