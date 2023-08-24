import asyncio
import pygame, sys
from random import choice, randint
from laser import Laser
from player import Player
from invaders import alien

'''
all classes definitions :
- laser
Laser(pos_x, pos_y, speed, constraint)

- Player
Player(pos_x, pos_y, constraint)

- invaders
Alien(pos_x, pos_y, constraint, color)

'''

async def main():
    class Game:
        def __init__(self):
            self.game_active = False
            self.game_state = 1

            self.lives = 3
            self.lives_surf = pygame.image.load('Graphics/spaceship.png')
            self.lives_surf = pygame.transform.rotozoom(self.lives_surf, 0, 0.1)
            self.lives_offset = 200

            self.background = pygame.image.load('Graphics/backgound.png')
            self.background = pygame.transform.rotozoom(self.background,0, times_factor)

            self.main_ship = Player(400, screen_height, screen_width*times_factor - 70)
            self.main_ship_group = pygame.sprite.GroupSingle(self.main_ship)

            self.alienGroup = pygame.sprite.Group()

            self.alien_lasers = pygame.sprite.Group()
            self.direction = 1
            #self.alien_setup()
            self.text_font = pygame.font.Font('font/RETRO_SPACE_INV.ttf', 40)
            self.text_font1 = pygame.font.Font('font/RETRO_SPACE_INV.ttf', 25)
            self.score = 0

            music = pygame.mixer.Sound('audio//backgroundMusic.ogg')
            music.set_volume(0.7)
            music.play(loops = -1)
            self.laser_sound = pygame.mixer.Sound('audio/laser4.ogg')
            self.laser_sound.set_volume(0.2)

        def alien_setup(self):
            if not self.alienGroup:
                number = randint(1,3)
                color = None
                if number == 1:
                    shape = ['xxzzzxx',
                             ' yyzyy ',
                             '  xyx  ',
                             '   x  ']
                    for row_ind, rows in enumerate(shape) :
                        for col_ind, cols in enumerate(rows):
                            if cols != ' ':
                                if cols == 'x':
                                   color = 'red'
                                if cols == 'y':
                                    color = 'yellow'
                                if cols == 'z':
                                    color = 'green'
                                self.aliens = alien(100 + col_ind * 43,50*2 + row_ind*33,screen_width*times_factor , color)
                                self.alienGroup.add(self.aliens)
                if number == 2:
                    shape = ['xyz zyx',
                             ' xyzyx ',
                             '  xyx  ',
                             '   x   ']
                    for row_ind, rows in enumerate(shape) :
                        for col_ind, cols in enumerate(rows):
                            if cols != ' ':
                                if cols == 'x':
                                   color = 'red'
                                if cols == 'y':
                                    color = 'yellow'
                                if cols == 'z':
                                    color = 'green'
                                self.aliens = alien(100 + col_ind * 43,50*2 + row_ind*33,screen_width*times_factor , color)
                                self.alienGroup.add(self.aliens)
                if number == 3:
                    shape = ['xzzzzzx',
                             'yyyyyyy ',
                             'x xyx x ',
                             '  xxx  ']
                    for row_ind, rows in enumerate(shape) :
                        for col_ind, cols in enumerate(rows):
                            if cols != ' ':
                                if cols == 'x':
                                   color = 'red'
                                if cols == 'y':
                                    color = 'yellow'
                                if cols == 'z':
                                    color = 'green'
                                self.aliens = alien(100 + col_ind * 43,50*2 + row_ind*33,screen_width*times_factor , color)
                                self.alienGroup.add(self.aliens)

        def alien_downward(self):
            sprites = self.alienGroup.sprites()
            for sprite in sprites:
                sprite.rect.y += 10

        def HUD(self):
            font = pygame.font.Font('font/RETRO_SPACE_INV.ttf', 25)
            text = font.render("SCORE : " + str(self.score),False, 'White')
            screen.blit(text, (0,0))
            text1 = font.render("Target : 600", False, 'White')

            screen.blit(text1,(screen_width - (40 * 3 + 70),0))
            x = screen_width/2 - 70
            for lives in range(self.lives):
                screen.blit(self.lives_surf, (x, self.lives_surf.get_size()[1]))
                x += 50

        def alien_position(self):
            sprites = self.alienGroup.sprites()
            for sprite in sprites:
                if sprite.rect.x >= screen_width - 42:
                    self.direction = -1
                    self.alien_downward()
                elif sprite.rect.x < 0:
                    self.direction = 1
                    self.alien_downward()

        def collisions(self):
            if self.main_ship_group.sprite.laser_group:
                for laser in self.main_ship_group.sprite.laser_group:
                    alien_collisions = pygame.sprite.spritecollide(laser, self.alienGroup, True)
                    for alien in alien_collisions:
                        laser.kill()
                        self.score += alien.score()
            if self.alien_lasers:
                for laser in self.alien_lasers:
                    if pygame.sprite.spritecollide(laser, self.main_ship_group, False):
                        laser.kill()
                        self.lives -= 1
                        if (self.lives <= 0):
                            print("========= GAME OVER ========== ")
                            self.game_state = 3
                            self.game_active = False

                # if pygame.sprite.spritecollide(lasers, self.main_ship_group, True):
                #     self.main_ship_group.empty()
                #     self.alienGroup.empty()
                #     self.game_active = False
                #     self.game_state = 3
                #     break

        def alien_shoot(self):
            if self.alienGroup.sprites():
                sprites = self.alienGroup.sprites()
                self.laser_sound.play()
                random_sprite = choice(sprites)
                selected_alien = random_sprite
                if (selected_alien.color == 'red'):
                    alien_laser = Laser(random_sprite.rect.midbottom[0], random_sprite.rect.midbottom[1], -5, screen_height)
                    self.alien_lasers.add(alien_laser)

                if (selected_alien.color == 'yellow'):
                    alien_laser = Laser(random_sprite.rect.midbottom[0], random_sprite.rect.midbottom[1], -8, screen_height)
                    self.alien_lasers.add(alien_laser)

                if (selected_alien.color == 'green'):
                    alien_laser = Laser(random_sprite.rect.midbottom[0], random_sprite.rect.midbottom[1], -10, screen_height)
                    self.alien_lasers.add(alien_laser)

        def state_manager(self):
            keys = pygame.key.get_pressed()

            if self.game_state == 1:
                if keys[pygame.K_b]:
                    self.game_active = True
                screen.blit(self.background, (0,0))
                text = self.text_font.render("STAR SHOOTER", False, 'Yellow')
                text1 = self.text_font1.render("Press B to start", False, 'White')
                screen.blit(text, (screen_width/2 - 150, screen_height/2 - 50))
                screen.blit(text1, (screen_width/2 - 150, screen_height/2 ))
            elif self.game_state == 2:
                screen.blit(self.background, (0,0))
                text3 = self.text_font.render("VICTORYS", False, 'Yellow')
                screen.blit(text3, (screen_width/2 - 150 + 50, screen_height/2 - 50))
                score_final = self.text_font1.render("SCORE : " + str(self.score),False, 'White')
                screen.blit(score_final,(screen_width/2 - 150 + 50, screen_height/2 - 50 + 50))
            elif self.game_state == 3:
                screen.blit(self.background, (0,0))
                text3 = self.text_font.render("GAME OVER", False, 'Yellow')
                screen.blit(text3, (screen_width/2 - 150 + 50, screen_height/2 - 50))
                score_final = self.text_font1.render("SCORE : " + str(self.score),False, 'White')
                screen.blit(score_final,(screen_width/2 - 150 + 50, screen_height/2 - 50 + 50))

        def score_target(self,score):
            if score >= 600:
                self.game_active = False
                self.game_state = 2

        def run(self):
            screen.blit(self.background, (0,0))
            self.alien_position()
            self.collisions()
            self.alien_setup()
            self.aliens = None
            self.HUD()
            self.score_target(self.score)

            self.main_ship_group.sprite.laser_group.update()
            self.main_ship_group.draw(screen)
            self.main_ship_group.update()

            self.main_ship_group.sprite.laser_group.draw(screen)
            self.alienGroup.draw(screen)
            self.alienGroup.update(self.direction)

            self.alien_lasers.draw(screen)
            self.alien_lasers.update()
            clock.tick(120)

    pygame.init()
    times_factor = 3
    screen_width = 272*times_factor
    screen_height = 160*times_factor

    screen = pygame.display.set_mode((screen_width, screen_height))
    title = pygame.display.set_caption('Star Shooter')
    clock = pygame.time.Clock()
    game = Game()

    ALIENSHOOT = pygame.USEREVENT + 1

    pygame.time.set_timer(ALIENSHOOT, randint(600, 1200))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.game_active:
                if event.type == ALIENSHOOT:
                    game.alien_shoot()


        if game.game_active:
            game.run()
        else:
            game.state_manager()


        clock.tick(120)
        pygame.display.update()
        
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())
