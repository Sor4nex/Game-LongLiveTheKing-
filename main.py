# imports
import pygame
import time as t
import sys
import random as r
import sqlite3

from pygame import image
from pygame.font import Font
from pygame.transform import scale
# /imports


# other functions
def game_boost_shop(screen):
    global cur, con
    gold = pygame.font.Font(None, 50)
    boost = pygame.font.Font(None, 50)
    money = cur.execute('SELECT money FROM user WHERE id = 1').fetchall()[0][0]
    freeze, clean, reload = cur.execute('SELECT freeze, clean, reload FROM boosts WHERE id = 1').fetchall()[0]
    money_text = gold.render('Монеты: ' + str(money), False, (255, 255, 0))
    fre_text = boost.render(str(freeze), False, (255, 255, 255))
    cle_text = boost.render(str(clean), False, (255, 255, 255))
    rel_text = boost.render(str(reload), False, (255, 255, 255))
    image = pygame.image.load('photo/Magaz.png')
    screen.blit(image, (0, 0))
    screen.blit(money_text, (700, 25))
    screen.blit(fre_text, (340, 215))
    screen.blit(rel_text, (585, 215))
    screen.blit(cle_text, (807, 215))

    while True:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    x, y = event.pos
                    if ((x > 179) and (x < 383)) and ((y > 373) and (y < 448)):
                        if (money >= 20):
                            freeze += 1
                            money -= 20
                            cur.execute('UPDATE user SET money = money - 20 WHERE id = 1')
                            cur.execute('UPDATE boosts SET freeze = freeze + 1 WHERE id = 1')
                            con.commit()
                        else:
                            pass
                    elif ((x > 387) and (x < 631)) and ((y > 373) and (y < 448)):
                        if (money >= 30):
                            reload += 1
                            money -= 30
                            cur.execute('UPDATE user SET money = money - 30 WHERE id = 1')
                            cur.execute('UPDATE boosts SET reload = reload + 1 WHERE id = 1')
                            con.commit()
                        else:
                            pass
                    elif ((x > 637) and (x < 834)) and ((y > 373) and (y < 448)):
                        if (money >= 15):
                            clean += 1
                            money -= 15
                            cur.execute('UPDATE user SET money = money - 15 WHERE id = 1')
                            cur.execute('UPDATE boosts SET clean = clean + 1 WHERE id = 1')
                            con.commit()
                        else:
                            pass
                    elif ((x > 7) and (x < 160)) and ((y > 12) and (y < 59)):
                        return
        money_text = gold.render('Монеты: ' + str(money), False, (255, 255, 0))
        fre_text = boost.render(str(freeze), False, (255, 255, 255))
        cle_text = boost.render(str(clean), False, (255, 255, 255))
        rel_text = boost.render(str(reload), False, (255, 255, 255))
        screen.blit(image, (0, 0))
        screen.blit(money_text, (700, 25))
        screen.blit(fre_text, (340, 215))
        screen.blit(rel_text, (585, 215))
        screen.blit(cle_text, (807, 215))
        pygame.display.flip()
        clock.tick(50)

def game_rules(screen):
    image = pygame.image.load('photo/rule.png')
    screen.blit(image, (0, 0))
    while True:
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    return
        pygame.display.flip()
        clock.tick(50)

def game_start_screen(screen) -> bool:
    global con, cur
    image = pygame.image.load('photo/start.png')
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 50)
    record_from_db = cur.execute('SELECT record FROM user WHERE id = 1').fetchall()[0][0]
    record = font.render(str(record_from_db), False, (255, 0, 0))
    screen.blit(record, (500, 75))
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                x, y = event.pos
                if ((x > 658) and (x < 982)) and ((y > 32) and (y < 112)):
                    return True
                elif ((x > 658) and (x < 982)) and ((y > 139) and (y < 220)):
                    game_boost_shop(screen)
                    image = pygame.image.load('photo/start.png')
                    screen.blit(image, (0, 0))
                    screen.blit(record, (500, 75))
                elif ((x > 658) and (x < 982)) and ((y > 242) and (y < 336)):
                    game_rules(screen)
                    image = pygame.image.load('photo/start.png')
                    screen.blit(image, (0, 0))
                    screen.blit(record, (500, 75))
                elif ((x > 39) and (x < 135)) and ((y > 415) and (y < 446)):
                    return False
        pygame.display.flip()
        clock.tick(50)

def game_death_screen(screen) -> bool:
    global time_now
    f2 = pygame.font.Font(None, 70)
    result = f2.render(str(time_now), False, (255, 255, 255))
    image = pygame.image.load('photo/death.png')
    screen.blit(image, (0, 0))
    screen.blit(result, (470, 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                x, y = event.pos
                if ((x > 46) and (x < 350)) and ((y > 321) and (y < 397)):
                    return True
                if ((x > 631) and (x < 936)) and ((y > 321) and (y < 397)):
                    return False
        pygame.display.flip()
        clock.tick(50)
# /other functions


# classes of game objects
class Character:  # A player character
    def __init__(self, x_pos, y_pos, width, skin) -> None:
        self.player_skin = skin
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.paused = False
    
    def show_entity_game(self, screen) -> None:
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.width)

    def set_new_entity_pos(self, plus_x, plus_y) -> None:
        if not(self.paused):
            self.x += plus_x
            self.y += plus_y
        else:
            pass
    
    def pause_motion(self, bool) -> None:
        self.paused = bool


class Bullet:  # A laser, that appears during the game
    def __init__(self) -> None:
        self.radio = 5
        self.paused = False
        start_x_choice = r.choice([0, 1, 2, 3])
        if (start_x_choice == 0):
            self.x, self.y = (0, r.randint(0, 500))
            self.speed_x = r.randint(0, 10)
            self.speed_y = r.randint(-5, 5)
        elif (start_x_choice == 1):
            self.x, self.y = (r.randint(0, 700), 0)
            self.speed_x = r.randint(-5, 5)
            self.speed_y = r.randint(0, 10)
        elif (start_x_choice == 2):
            self.x, self.y = (700, r.randint(0, 500))
            self.speed_x = r.randint(-10, 0)
            self.speed_y = r.randint(-5, 5)
        elif (start_x_choice == 3):
            self.x, self.y = (r.randint(0, 700), 500)
            self.speed_x = r.randint(-5, 5)
            self.speed_y = r.randint(-10, 0)


    def show_entity_game(self, screen) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radio)
    
    def set_new_entity_pos(self) -> None:
        if not(self.paused):
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            pass

    def pause_motion(self, bool) -> None:
        self.paused = bool
# /classes of game objects


# game main script
if (__name__ == '__main__'):
    # window set up
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    app_running = True
    con = sqlite3.connect('db/game.db')
    cur = con.cursor()
    f1 = pygame.font.Font(None, 50)
    f2 = pygame.font.Font(None, 25)
    fre_font = pygame.font.Font(None, 40)
    pygame.display.set_caption('LongLiveTheKing')
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    # /window set up
    
    while app_running:
        app_running = game_start_screen(screen)
        # variables
        running = True
        moving_x_up = False
        moving_y_up = False
        moving_x_down = False
        moving_y_down = False
        bullets_on_screen = list()
        counter = 0
        time_was = 0
        time_now = 0
        money_earned = 0
        bullet_count = 3
        pause_countdown = 4
        game_paused = False
        img_fre = pygame.image.load('photo/fre.png')
        img_cle = pygame.image.load('photo/cle.png')
        img_rel = pygame.image.load('photo/rel.png')
        img_fre = pygame.transform.scale(img_fre, (50, 50))
        img_cle = pygame.transform.scale(img_cle, (50, 50))
        img_rel = pygame.transform.scale(img_rel, (50, 50))
        record_now = cur.execute('SELECT record FROM user WHERE id = 1').fetchall()[0][0]
        freeze, clean, reload = cur.execute('SELECT freeze, clean, reload FROM boosts WHERE id = 1').fetchall()[0]
        # /variables

        # game set up
        player_character = Character(350, 350, 8, 'Normal')
        # game set up

        # game
        if (app_running == False):
            break
        while (running):
            # events
            for event in pygame.event.get():  # event checker. Get all events, done by player
                if (event.type == pygame.QUIT):
                    running = False
                    app_running = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_d):
                            moving_x_up = True
                    if (event.key == pygame.K_a):
                            moving_x_down = True
                    if (event.key == pygame.K_w):
                            moving_y_up = True
                    if (event.key == pygame.K_s):
                            moving_y_down = True
                    if (event.key == pygame.K_SPACE):
                        if (clean != 0):
                            clean -= 1
                            bullets_on_screen.clear()
                    if (event.key == pygame.K_r):
                        if (reload != 0) and (bullet_count >= 3):
                            reload -= 1
                            bullet_count -= 2
                    if (event.key == pygame.K_f):
                        if (freeze != 0):
                            freeze -= 1
                            game_paused = True
                            pause_countdown = 3
                            pause_countdown_text = fre_font.render(str(pause_countdown), False, (0, 0, 255))
                            screen.blit(pause_countdown_text, (670, 30))
                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_d):
                        moving_x_up = False
                    if (event.key == pygame.K_a):
                        moving_x_down = False
                    if (event.key == pygame.K_w):
                        moving_y_up = False
                    if (event.key == pygame.K_s):
                        moving_y_down = False
            # /events
            
            # player movements
            if (moving_x_up):
                if (player_character.x + 8 < 700):
                    player_character.set_new_entity_pos(8, 0)
            if (moving_x_down):
                if (player_character.x - 8 > 0):
                    player_character.set_new_entity_pos(-8, 0)
            if (moving_y_up):
                if (player_character.y - 8 > 0):
                    player_character.set_new_entity_pos(0, -8)
            if (moving_y_down):
                if (player_character.y + 8 < 500):
                    player_character.set_new_entity_pos(0, 8)
            # /player movements

            # time checker
            if (time_now % 10 == 0) and (time_now != 0) and (time_now != time_was):
                bullet_count += 2
                money_earned += 10
            if (time_now != time_was):
                if not(game_paused):
                    for bullet in range(bullet_count):
                        new = Bullet()
                        bullets_on_screen.append(new)
                else:
                    pause_countdown -= 1
            # /time checker

            # bullet movements and death
            if (pause_countdown == 0):
                game_paused = False
            for bullet in bullets_on_screen:
                if not(game_paused):
                    bullet.set_new_entity_pos()
                if ((player_character.x > bullet.x - 13) and (player_character.x < bullet.x + 13)) and (player_character.y > bullet.y - 13) and (player_character.y < bullet.y + 13):
                    new_record = time_now
                    cur.execute('UPDATE user SET record = ? WHERE record < ?', (new_record, new_record))
                    cur.execute('UPDATE user SET money = money + ? WHERE id = 1', (money_earned, ))
                    cur.execute('UPDATE boosts SET freeze = ?, clean = ?, reload = ? WHERE id = 1', (freeze, clean, reload))
                    con.commit()
                    running = False
                    app_running = game_death_screen(screen)
                    break
                if (bullet.x > 705) or (bullet.y > 505) or (bullet.x < -5) or (bullet.y < -5):
                    bullets_on_screen.remove(bullet)
                bullet.show_entity_game(screen)
            # /bullet movements and death

            # rendering
            player_character.show_entity_game(screen)
            clock.tick(60)
            time_was = time_now
            counter += 1
            if (counter % 60 == 0):
                time_now = counter // 60
            timer = f1.render(str(time_now), False, (255, 255, 255))
            text1 = f1.render('Время:', False, (255, 255, 255))
            text2 = f1.render('Рекорд:', False, (0, 255, 0))
            text3 = f2.render('Пуль в секунду:', False, (255, 0, 0))
            text4 = f2.render('Монет получено:', False, (255, 207, 64))
            record_text = f1.render(str(record_now), False, (0, 255, 0))
            money_text = f1.render(str(money_earned), False, (255, 207, 64))
            bullet_text = f1.render(str(bullet_count), False, (255, 0, 0))
            cle = f1.render(str(clean), False, (255, 255, 255))
            fre = f1.render(str(freeze), False, (255, 255, 255))
            rel = f1.render(str(reload), False, (255, 255, 255))
            screen.blit(text2, (720, 60))
            screen.blit(text1, (720, 10))
            screen.blit(text3, (720, 330))
            screen.blit(text4, (720, 380))
            screen.blit(timer, (900, 10))
            screen.blit(record_text, (900, 60))
            screen.blit(money_text, (900, 380))
            screen.blit(bullet_text, (900, 330))
            screen.blit(cle, (900, 110))
            screen.blit(fre, (900, 190))
            screen.blit(rel, (900, 270))
            screen.blit(img_cle, (720, 110))
            screen.blit(img_fre, (720, 190))
            screen.blit(img_rel, (720, 270))
            if (game_paused):
                    pause_countdown_text = fre_font.render(str(pause_countdown), False, (0, 0, 255))
                    screen.blit(pause_countdown_text, (670, 30))
            pygame.draw.line(screen, (255, 0, 0), (700, 0), (700, 500), 3)
            pygame.display.flip()
            screen.fill((0, 0, 0))
            # /rendering
    pygame.quit()
    # /game
# /game main script
