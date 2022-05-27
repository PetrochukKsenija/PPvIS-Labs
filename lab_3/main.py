# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import pygame
import pygame as pg
import json
from pygame.locals import *
from random import randrange as rnd
import pygame_menu

pygame.init()
display_width = 1200
display_height = 600
fps = 60
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Арканоид')
pg.mixer.music.load('fon.ogg')
tick = pg.mixer.Sound('tick.ogg')
block = pg.mixer.Sound('block.ogg')
clock = pygame.time.Clock()
with open("name.json", "r") as read_file1:
    name = json.load(read_file1)
with open("result.json", "r") as read_file2:
    best_result = json.load(read_file2)
yes = 0
result = 0

class Management:
    def __init__(self):
        pass

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()

class Blocks(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.blocks_list = []
        self.blocks_color_list = []

    def draw_polygon(self):
        [pygame.draw.rect(game_display, self.blocks_color_list[color], block)
         for color, block in enumerate(self.blocks_list)]

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.platform_w = 300
        self.platform_h = 20
        self.platform_speed = 15
        self.platform = pygame.Rect(display_width // 2 - self.platform_w // 2, display_height - self.platform_h - 10,
                                    self.platform_w, self.platform_h)

    def draw_platform(self):
        pygame.draw.rect(game_display, (250, 250, 250), self.platform)

    def control_platform(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.platform.left > 0:
            self.platform.left -= self.platform_speed
        if key[pygame.K_RIGHT] and self.platform.right < display_width:
            self.platform.right += self.platform_speed

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ball_radius = 15
        self.ball_speed = 7
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(display_width // 2, display_height * 7 // 8, self.ball_rect, self.ball_rect)
        self.dx = 1
        self.dy = -1

    def draw_ball(self):
        pygame.draw.circle(game_display, (250, 250, 250), self.ball.center, self.ball_radius)

    def movement_ball(self):
        self.ball.x += self.ball_speed * self.dx
        self.ball.y += self.ball_speed * self.dy

    def control_ball(self):
        if self.ball.centerx < self.ball_radius or self.ball.centerx > display_width - self.ball_radius:
            tick.play()
            self.dx = -self.dx
        if self.ball.centery < self.ball_radius:
            tick.play()
            self.dy = -self.dy

        if self.ball.bottom > display_height:
            pg.mixer.music.stop()
            level_loss()

    def detect_collision(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left

        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 5:
            dx = -dx
            dy = -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def collision_ball(self, platform, blocks_list, color_list, mod_type):
        if self.ball.colliderect(platform) and self.dy > 0:
            tick.play()
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, platform)

        hit_index = self.ball.collidelist(blocks_list)
        if hit_index != -1:
            block.play()
            hit_rect = blocks_list.pop(hit_index)
            color_list.pop(hit_index)
            num = random.randint(0, 4)
            mod_type.append(num)
            global yes, result
            yes = 1
            result += 10
            if not len(blocks_list):
                yes = 0
                pg.mixer.music.stop()
                if result >= best_result[0]:
                    input_name()
                level_win()

            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, hit_rect)

class Modifications(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.location_x = 0
        self.location_y = 0
        self.mod_speed = 2
        self.mod_side = 20
        self.mod_color = (225, 225, 225)
        self.mod_list = []
        self.mod_color_list = []
        self.mod_type = []

    def draw_modification(self):
        [pygame.draw.rect(game_display, self.mod_color_list[color], mod)
         for color, mod in enumerate(self.mod_list)]

    def movement_modification(self):
        for mod in self.mod_list:
            mod.y += self.mod_speed

    def choice_modification(self):
        num = self.mod_type[-1]
        if num == 0:
            mod = Platform_Reduction()
        elif num == 1:
            mod = Platform_Increase()
        elif num == 2:
            mod = Speed_Of_Ball_Reduction()
        elif num == 3:
            mod = Speed_Of_Ball_Increase()
        else:
            mod = Coin()
        self.location_x = mod.location_x
        self.mod_color = mod.color
        rect = pygame.Rect(self.location_x, self.location_y, self.mod_side, self.mod_side)
        self.mod_list.append(rect)
        self.mod_color_list.append(self.mod_color)

    def collision_mod(self, platform, ball):
        for mod in self.mod_list:
            if mod.colliderect(platform):
                hit_index = self.mod_list.index(mod)
                self.mod_list.pop(hit_index)
                self.mod_color_list.pop(hit_index)
                hit_mod_type = self.mod_type.pop(hit_index)
                if hit_mod_type == 0:
                    type = Platform_Reduction()
                    type.action(platform)
                elif hit_mod_type == 1:
                    type = Platform_Increase()
                    type.action(platform)
                elif hit_mod_type == 2:
                    type = Speed_Of_Ball_Reduction()
                    type.action(ball)
                elif hit_mod_type == 3:
                    type = Speed_Of_Ball_Increase()
                    type.action(ball)
                elif hit_mod_type == 4:
                    type = Coin()
                    type.action()

#уменьшение платформы
class Platform_Reduction():
    def __init__(self):
        self.location_x = rnd(0,1180)
        self.color = (225, 0, 0)

    def action(self, platform):
        if platform.width > 50:
            platform.width -= 50

#увеличение платформы
class Platform_Increase():
    def __init__(self):
        self.location_x = rnd(0,1180)
        self.color = (0, 225, 0)

    def action(self, platform):
        if platform.width < 1000:
            platform.width += 50

#уменьшение скорости шара
class Speed_Of_Ball_Reduction():
    def __init__(self):
        self.location_x = rnd(0, 1180)
        self.color = (225, 0, 225)

    def action(self, ball):
        if ball.ball_speed > 2:
            ball.ball_speed -= 1

#увеличение скорости шара
class Speed_Of_Ball_Increase():
    def __init__(self):
        self.location_x = rnd(0, 1180)
        self.color = (0, 225, 225)

    def action(self, ball):
        ball.ball_speed += 1

#монеты
class Coin():
    def __init__(self):
        self.location_x = rnd(0, 1180)
        self.color = (225, 225, 0)

    def action(self):
        global result
        result += random.randint(1, 50)
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def level_win():
    win = pygame_menu.Menu('Уровень пройден!', 400, 300,
                            theme=pygame_menu.themes.THEME_SOLARIZED)

    # win.add.button('')
    win.add.button('Выбор уровня', level_page1)
    win.add.button('Главное меню', main_menu)
    win.mainloop(game_display)

def level_loss():
    loss = pygame_menu.Menu('Вы проиграли!', 400, 300,
                            theme=pygame_menu.themes.THEME_SOLARIZED)

    # win.add.button('')
    loss.add.button('Выбор уровня', level_page1)
    loss.add.button('Главное меню', main_menu)
    loss.mainloop(game_display)

def level_page1():
    # blocks = Blocks()
    lev1 = pygame_menu.Menu('Выбор уровня', 400, 500,
                            theme=pygame_menu.themes.THEME_SOLARIZED)

    lev1.add.button('Уровень 1', level_1)
    lev1.add.button('Уровень 2', level_2)
    lev1.add.button('Уровень 3', level_3)
    lev1.add.button('Уровень 4', level_4)
    lev1.add.button('Уровень 5', level_5)
    lev1.add.button('Далее>>', level_page2)
    lev1.add.button('Главное меню', main_menu)
    lev1.mainloop(game_display)

def level_page2():
    lev2 = pygame_menu.Menu('Выбор уровня', 400, 500,
                           theme=pygame_menu.themes.THEME_SOLARIZED)

    lev2.add.button('Уровень 6', level_6)
    lev2.add.button('Уровень 7', level_7)
    lev2.add.button('Уровень 8', level_8)
    lev2.add.button('Уровень 9', level_9)
    lev2.add.button('Уровень 10', level_10)
    lev2.add.button('<<Назад', level_page1)
    lev2.add.button('Главное меню', main_menu)
    lev2.mainloop(game_display)

def level_1():
    blocks = Blocks()
    blocks.blocks_list = [pygame.Rect(120 * i + 5, 60 * j, 110, 50) for i in range(10) for j in range(4)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
    start_the_game(blocks)

def level_2():
    blocks = Blocks()
    blocks.blocks_list = [pygame.Rect(110 * i * 2, 65 * j, 110, 50) for i in range(6) for j in range(4)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(6) for j in range(4)]
    start_the_game(blocks)

def level_3():
    blocks = Blocks()
    blocks.blocks_list = [pygame.Rect(120 * i + 5, 50 * j * 2, 110, 50) for i in range(10) for j in range(3)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(3)]
    start_the_game(blocks)

def level_4():
    blocks = Blocks()
    blocks.blocks_list = [pygame.Rect(75 * i * 2 + 20, 50 * j * 2, 105, 50) for i in range(8) for j in range(3)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(8) for j in range(3)]
    start_the_game(blocks)

def level_5():
    blocks = Blocks()
    a = [0, 1, 0, 1]
    blocks.blocks_list = [pygame.Rect(120 * i * 2 + 120 * a[j], 50 * j, 120, 50) for i in range(5) for j in range(4)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(5) for j in range(4)]
    start_the_game(blocks)

def level_6():
    blocks = Blocks()
    blocks.blocks_list = [pygame.Rect(110 * i * 2 + 60 * j + 16, 60 * j, 110, 50) for i in range(5) for j in range(4)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(5) for j in range(4)]
    start_the_game(blocks)

def level_7():
    blocks = Blocks()
    a = [0, 1, 0, 1]
    blocks.blocks_list = [pygame.Rect(120 * i * 2 + 60 * a[j] + 30, 55 * j, 110, 50) for i in range(5) for j in range(4)]
    blocks.blocks_color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(5) for j in range(4)]
    start_the_game(blocks)

def level_8():
    blocks = Blocks()
    sum = 10
    for j in range(5):
        for i in range(sum):
            block = pygame.Rect(120 * i + 5 + 60 * (10 - sum), 60 * j, 110, 50)
            blocks.blocks_list.append(block)
            blocks.blocks_color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
        sum = sum - 2
    start_the_game(blocks)

def level_9():
    blocks = Blocks()
    sum = 2
    number = 0
    for j in range(4):
        for i in range(sum):
            if number < sum / 2:
                block = pygame.Rect(120 * i + 10, 60 * j, 110, 50)
                blocks.blocks_list.append(block)
                blocks.blocks_color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
                number = number + 1
            else:
                block = pygame.Rect(120 * i + 120 * (10 - sum), 60 * j, 110, 50)
                blocks.blocks_list.append(block)
                blocks.blocks_color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
        sum = sum + 2
        number = 0
    start_the_game(blocks)

def level_10():
    blocks = Blocks()
    sum = 10
    number = 0
    for j in range(5):
        for i in range(sum):
            if number < sum / 2:
                block = pygame.Rect(120 * i + 5, 60 * j, 110, 50)
                blocks.blocks_list.append(block)
                blocks.blocks_color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
                number = number + 1
            else:
                block = pygame.Rect(120 * i + 120 * (10 - sum) + 5, 60 * j, 110, 50)
                blocks.blocks_list.append(block)
                blocks.blocks_color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
        sum = sum - 2
        number = 0
    start_the_game(blocks)

def reference():
    ref = pygame_menu.Menu('Справка', 650, 550,
                            theme=pygame_menu.themes.THEME_SOLARIZED)
    ref.add.label('Арканоид')
    ref.add.label('Принцип игры: с помощью клавиш влево')
    ref.add.label('и вправо необходимо двигать платформу')
    ref.add.label('от которой будет отскакивать мяч и')
    ref.add.label('разбивать блоки.')
    ref.add.label('Задача игрока - разбить все блоки')
    ref.add.label('и не дать мячу упасть')
    ref.add.label('В игре существуют модификаторы,')
    ref.add.label('появляющиеся после разбиения блока.')
    ref.add.label('Типы подификаторов:')
    ref.add.label('красный - уменьшение платформы')
    ref.add.label('зеленый - увеличение платформы')
    ref.add.label('желтый - дополнительные баллы')
    ref.add.label('голубой - увеличение скорости мяча')
    ref.add.label('розовый - уменьшение скорости мяча.')
    ref.add.button('Главное меню', main_menu)
    ref.mainloop(game_display)

def start_the_game(blocks):
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1)
    global result
    result = 0
    management = Management()
    platform = Platform()
    ball = Ball()
    mod = Modifications()
    while True:
        management.event_handler()
        game_display.fill((0, 0, 0))

        blocks.draw_polygon()

        platform.control_platform()
        platform.draw_platform()

        ball.movement_ball()
        ball.control_ball()
        ball.collision_ball(platform.platform, blocks.blocks_list, blocks.blocks_color_list, mod.mod_type)
        ball.draw_ball()

        mod.draw_modification()
        mod.movement_modification()
        global yes
        if yes == 1:
            mod.choice_modification()
            yes = 0
        mod.collision_mod(platform.platform, ball)

        pygame.display.flip()
        clock.tick(fps)
    pass

def main_menu():
    menu = pygame_menu.Menu('Меню', 400, 300,
                            theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('Начать игру', level_page1)
    menu.add.button('Таблица рекордов', table)
    menu.add.button('Справка', reference)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(game_display)

def input_name():
    menu = pygame_menu.Menu('Меню', 400, 300,
                            theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label('Вы побили рекорд!!!')
    menu.add.text_input('Ведите имя: ', default='Игрок 1', onreturn=Name)
    menu.add.button('Далее', level_win)
    menu.mainloop(game_display)

def Name(value):
    global name
    name.insert(0, value)
    name.pop(5)
    with open("name.json", "w") as write_file_1:
        json.dump(name, write_file_1)
    global best_result, result
    best_result.insert(0, result)
    best_result.pop(5)
    with open("result.json", "w") as write_file_2:
        json.dump(best_result, write_file_2)
    result = 0

def table():
    menu = pygame_menu.Menu('Меню', 400, 400,
                            theme=pygame_menu.themes.THEME_SOLARIZED)
    table = menu.add.table(table_id='my_table', font_size=23)
    table.default_cell_padding = 7
    table.add_row(['Name', 'Result'],
                  cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

    table.add_row([name[0], best_result[0]], cell_align=pygame_menu.locals.ALIGN_CENTER)
    table.add_row([name[1], best_result[1]], cell_align=pygame_menu.locals.ALIGN_CENTER)
    table.add_row([name[2], best_result[2]], cell_align=pygame_menu.locals.ALIGN_CENTER)
    table.add_row([name[3], best_result[3]], cell_align=pygame_menu.locals.ALIGN_CENTER)
    table.add_row([name[4], best_result[4]], cell_align=pygame_menu.locals.ALIGN_CENTER)
    menu.add.button('Главное меню', main_menu)
    menu.mainloop(game_display)

if __name__ == '__main__':
    main_menu()