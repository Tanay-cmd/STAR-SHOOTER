import pygame
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, constraint):
        super().__init__()
        self.image = pygame.image.load('Graphics//spaceship.png')
        self.image = pygame.transform.rotozoom(self.image, 0, 0.13)
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.speed = 3
        self.recharge = 600
        self.ready = True
        self.shoot_instant = 0
        self.constraint = constraint
        self.laser_group = pygame.sprite.Group()
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.ready == True:
            self.shoot_instant = pygame.time.get_ticks()
            self.shoot()
            laser_sound = pygame.mixer.Sound('audio//laser1.ogg')
            laser_sound.set_volume(0.2)
            laser_sound.play()
            self.ready = False
    def shoot(self):
        self.laser_group.add(self.create_bullet())
    def create_bullet(self):
        return Laser(self.rect.midtop[0], self.rect.midtop[1], 5, 272*3 + 30, 1)
    def reload(self):
        if not self.ready:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.shoot_instant >= 600:
                self.ready = True
    def boundary(self):
        if (self.rect.x >= self.constraint):
            self.rect.x = self.constraint
        if self.rect.x < 0:
            self.rect.x = 0
    def update(self):
        self.input()  
        self.boundary()
        self.reload()
        self.laser_group.update()
        
