import pygame
import os
import random
from items.bomb import Bomb
from items.heart import Heart
from items.missile import Missile
from items.widebullet_item import WideBulletItem

class ItemSpawner:
    def __init__(self):
        self.item_group = pygame.sprite.Group()
        self.can_spawnItem = True
    
    def update(self):
        self.item_group.update()
    
    def spawn_item(self,x,y):
        if self.can_spawnItem:
            rand_spawn = random.randrange(1,100)
            if rand_spawn >= 80:
                rand_item = random.randrange(1,100)
                if rand_item < 25: #<25
                    new_item = Bomb(x,y)
                elif rand_item >= 25 and rand_item < 50: # >=25 and <50
                    new_item = Heart(x,y)
                elif rand_item >= 50 and rand_item < 75:
                    new_item = Missile(x,y)
                elif rand_item >= 75 and rand_item < 100:
                    new_item = WideBulletItem(x,y)
                
                self.item_group.add(new_item)
        