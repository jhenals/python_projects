import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25
cactus_img = pygame.image.load('cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SHEvsJHE')


class Topscore:
    def __init__(self):
        self.high_score = 0

    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score


topscore = Topscore()


class Jhena:
    jhena_velocity = 10

    def __init__(self):
        self.jhena_img = pygame.image.load('char2.png')
        self.jhena_img_rect = self.jhena_img.get_rect()
        self.jhena_img_rect.width -= 10
        self.jhena_img_rect.height -= 10
        self.jhena_img_rect.top = WINDOW_HEIGHT/2
        self.jhena_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.jhena_img, self.jhena_img_rect)
        if self.jhena_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.jhena_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.jhena_img_rect.top -= self.jhena_velocity
        elif self.down:
            self.jhena_img_rect.top += self.jhena_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = jhena.jhena_img_rect.left
        self.flames_img_rect.top = jhena.jhena_img_rect.top + 30

    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class She:
    velocity = 10

    def __init__(self):
        self.she_score = None
        self.she_img = pygame.image.load('char1.png')
        self.she_img_rect = self.she_img.get_rect()
        self.she_img_rect.left = 20
        self.she_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.she_img, self.she_img_rect)
        if self.she_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.she_score:
                self.she_score = SCORE
        if self.she_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.she_score:
                self.she_score = SCORE
        if self.up:
            self.she_img_rect.top -= 10
        if self.down:
            self.she_img_rect.bottom += 10


def terminate():
    pygame.quit()
    sys.exit()


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('mario_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('s_j_end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                terminate()
            if EVENT.key == pygame.K_ESCAPE:
                terminate()
            music.stop()
            game_loop()
        pygame.display.update()

def check_level(score):
    global LEVEL
    if SCORE in range(0,10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT -100
        LEVEL= 2
    elif SCORE in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('s_j_start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    terminate()
                game_loop()
        pygame.display.update()


def game_loop():
    while True:
        global jhena
        jhena = Jhena()
        flames = Flames()
        she = She()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('mario_theme.wav')
        pygame.mixer.music.play(-1,0.0)
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            jhena.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        she.up = True
                        she.down = False
                    elif event.key == pygame.K_DOWN:
                        she.down = True
                        she.up= False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        she.up = True
                        she.down = False
                    elif event.key == pygame.K_DOWN:
                        she.down = True
                        she.up= False
            score_font = font.render('Score:' + str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            she.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(she.she_img_rect):
                    game_over()
                    if SCORE > she.she_score:
                        she.she_score = SCORE

            pygame.display.update()
            CLOCK.tick(FPS)

start_game()