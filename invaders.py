import pygame
pygame.init()
from laser import Laser
class alien(pygame.sprite.Sprite):
    def __init__(self, x, y, constraint, color):
        super().__init__()
        path = 'Graphics//'+ color +'.png'
        self.image = pygame.image.load(path)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 1
        self.color = color
        self.boundary = constraint
    def score(self):
        
        if self.color == 'red':
            return 10
        if self.color == 'yellow':
            return 30
        if self.color == 'green':
            return 50
        
        
    def update(self, direction):
        self.rect.x += direction
        

       
            



    
