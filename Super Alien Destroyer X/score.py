import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score,self).__init__()
        self.font = pygame.font.SysFont('arial',26)
        self.text = self.font.render('Score : ',True, (255,255,255))
        self.x = 1000
        self.y = 0
        
    def update(self):
        self.text = self.font.render('Score : ',True, (255,255,255))
