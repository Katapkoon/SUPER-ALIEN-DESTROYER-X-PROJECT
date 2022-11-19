import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score,self).__init__()
        self.score_num = 0
        self.font = pygame.font.SysFont('arial',26)
        self.text = self.font.render('Score : ' + str(self.score_num),True, (255,255,255))
        self.x = 1000
        self.y = 0
        
    def update(self):
        self.text = self.font.render('Score : ' + str(self.score_num),True, (255,255,255))
