# imports
import pygame
import time as t
import sys
import random as r
import sqlite3 as sql
# /imports


# classes of game objects
class Entity:  # parent class
    def __init__(self, x_pos, y_pos, x_width, y_width, type_scucture=None) -> None:
        self.pos_entity_x = x_pos
        self.pos_entity_y = y_pos
        self.x_width = x_width
        self.y_width = y_width
        self.type_structure = type_scucture

    def show_entity_game(self, screen) -> None:  # shows all objects of game, you can interact with
        if (self.type_structure is None):
            pygame.draw.ellipse(screen, (255, 0, 0), (self.pos_entity_x, self.pos_entity_y, self.x_width, self.y_width))

    def set_new_entity_pos(self, pos_x=0, pos_y=0) -> None: # updates entity position (self.pos_entity_x = x_pos, self.pos_entity_y = y_pos)
        self.pos_entity_x += pos_x
        self.pos_entity_y += pos_y


class Character(Entity):  # A player character
    def __init__(self, x_pos, y_pos, x_width, y_width, skin) -> None:
        super().__init__(x_pos, y_pos, x_width, y_width)
        self.player_skin = skin


class Laser:  # A laser, that appears during the game
    def __init__(self, start_x, start_y, end_x, end_y) -> None:
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def check_hit_laser(self) -> bool:  # checks if smth stands in way of laser of touches it
        pass


class Enemy(Entity):  # A chasing enemies
    def __init__(self, x_pos, y_pos, x_width, y_width, type_structure) -> None:
        super().__init__(x_pos, y_pos, x_width, y_width, type_structure)
        self.type_structure = type_structure
# /classes of game objects


# game main script
if (__name__ == '__main__'):
    # window set up
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
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
    objects_on_screen = list()
    counter = 0
    # /variables

    # game set up
    player_character = Character(350, 350, 30, 20, 'Normal')
    objects_on_screen.append(player_character)
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
        for object in objects_on_screen:
            object.show_entity_game(screen)
        clock.tick(60)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    # /game
# /game main script
