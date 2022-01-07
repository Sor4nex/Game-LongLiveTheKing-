# imports
import pygame
import time as t
import sys
import random as r
import sqlite3 as sql
# /imports


# classes of game objects
class Character:  # A player character
    def __init__(self, x_pos, y_pos, width, skin) -> None:
        self.player_skin = skin
        self.x = x_pos
        self.y = y_pos
        self.width = width
    
    def show_entity_game(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.width)

    def set_new_entity_pos(self, plus_x, plus_y):
        self.x += plus_x
        self.y += plus_y


class Bullet:  # A laser, that appears during the game
    def __init__(self) -> None:
        self.radio = 5
        start_x_choice = r.choice([0, 1, 2, 3])
        if (start_x_choice == 0):
            self.x, self.y = (0, r.randint(0, 500))
            self.speed_x = r.randint(0, 10)
            self.speed_y = r.randint(-5, 5)
        elif (start_x_choice == 1):
            self.x, self.y = (r.randint(0, 500), 0)
            self.speed_x = r.randint(-5, 5)
            self.speed_y = r.randint(0, 10)
        elif (start_x_choice == 2):
            self.x, self.y = (500, r.randint(0, 500))
            self.speed_x = r.randint(-10, 0)
            self.speed_y = r.randint(-5, 5)
        elif (start_x_choice == 3):
            self.x, self.y = (r.randint(0, 500), 500)
            self.speed_x = r.randint(-5, 5)
            self.speed_y = r.randint(-10, 0)


    def show_entity_game(self, screen) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radio)
    
    def set_new_entity_pos(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def check_hit_bullet(self) -> bool:  # checks if smth stands in way of laser of touches it
        pass
# /classes of game objects


# game main script
if (__name__ == '__main__'):
    # window set up
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('LongLiveTheKing')
    screen.fill((0, 0, 0))
    # /window set up

    # variables
    running = True
    moving_x_up = False
    moving_y_up = False
    moving_x_down = False
    moving_y_down = False
    clock = pygame.time.Clock()
    bullets_on_screen = list()
    counter = 0
    time_was = 0
    time_now = 0
    bullet_count = 1
    # /variables

    # game set up
    player_character = Character(350, 350, 8, 'Normal')
    # game set up

    # game
    while (running):
        for event in pygame.event.get():  # event checker. Get all events, done by player
            if (event.type == pygame.QUIT):
                running = False
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_d):
                        moving_x_up = True
                if (event.key == pygame.K_a):
                        moving_x_down = True
                if (event.key == pygame.K_w):
                        moving_y_up = True
                if (event.key == pygame.K_s):
                        moving_y_down = True
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_d):
                    moving_x_up = False
                if (event.key == pygame.K_a):
                    moving_x_down = False
                if (event.key == pygame.K_w):
                    moving_y_up = False
                if (event.key == pygame.K_s):
                    moving_y_down = False
        if (moving_x_up):
            player_character.set_new_entity_pos(8, 0)
        if (moving_x_down):
            player_character.set_new_entity_pos(-8, 0)
        if (moving_y_up):
            player_character.set_new_entity_pos(0, -8)
        if (moving_y_down):
            player_character.set_new_entity_pos(0, 8)
        if (time_now % 10 == 0) and (time_now != 0) and (time_now != time_was):
            bullet_count += 1
        if (time_now != time_was):
            for bullet in range(bullet_count):
                new = Bullet()
                bullets_on_screen.append(new)
        for bullet in bullets_on_screen:
            bullet.set_new_entity_pos()
            if ((player_character.x > bullet.x) and (player_character.x < bullet.x + 15)) and (player_character.y > bullet.y) and (player_character.y < bullet.y + 15):
                print('lose')
            if (bullet.x > 500) or (bullet.y > 500) or (bullet.x < 0) or (bullet.y < 0):
                bullets_on_screen.remove(bullet)
            bullet.show_entity_game(screen)
        player_character.show_entity_game(screen)
        clock.tick(60)
        time_was = time_now
        counter += 1
        if (counter % 60 == 0):
            time_now = counter // 60
            print(time_now)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    # /game
# /game main script
