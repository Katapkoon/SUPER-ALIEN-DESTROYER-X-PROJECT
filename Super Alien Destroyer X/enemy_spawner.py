import pygame
from enemy import Enemy
from enemy2 import Golem
from enemy3 import SideEnemy
import random

class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = random.randrange(20,60)
    
    def update(self):
        self.enemy_group.update()
        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = random.randrange(20,60) #20,60
        else:
            self.spawn_timer -= 1

    def spawn_enemy(self):
        random_number = random.randrange(0,100)
        if random_number <= 60:
            new_enemy = Enemy()
        elif random_number > 60 and random_number <= 90:
            new_enemy = SideEnemy()
        elif random_number > 90:
            new_enemy = Golem()
    
        self.enemy_group.add(new_enemy)