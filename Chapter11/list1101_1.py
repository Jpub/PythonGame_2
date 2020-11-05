import pygame
import sys
import math
import random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 224, 0)

tmr = 0

DATA_LR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0, -2, -2, -4, -4, -2, -1, 0, 0, 0, 0, 0, 0, 0]
DATA_UD = [0, 0, 1, 2, 3, 2, 1, 0, -2, -4, -2, 0, 0, 0, 0, 0, -1, -2, -3, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, -6, 6, 0]
CLEN = len(DATA_LR)

BOARD = 120
CMAX = BOARD * CLEN
curve = [0] * CMAX
updown = [0] * CMAX
object_left = [0] * CMAX
object_right = [0] * CMAX

CAR = 30
car_x = [0] * CAR
car_y = [0] * CAR
car_lr = [0] * CAR
car_spd = [0] * CAR
PLCAR_Y = 10  # 플레이어 차량 표시 위치, 가장 가까운 도로(화면 아래)가 0


def make_course():
    for i in range(CLEN):
        lr1 = DATA_LR[i]
        lr2 = DATA_LR[(i + 1) % CLEN]
        ud1 = DATA_UD[i]
        ud2 = DATA_UD[(i + 1) % CLEN]
        for j in range(BOARD):
            pos = j + BOARD * i
            curve[pos] = lr1 * (BOARD - j) / BOARD + lr2 * j / BOARD
            updown[pos] = ud1 * (BOARD - j) / BOARD + ud2 * j / BOARD
            if j == 60:
                object_right[pos] = 1  # 간판
            if i % 8 < 7:
                if j % 12 == 0:
                    object_left[pos] = 2  # 야자 나무
            else:
                if j % 20 == 0:
                    object_left[pos] = 3  # 요트
            if j % 12 == 6:
                object_left[pos] = 9  # 바다


def draw_obj(bg, img, x, y, sc):
    img_rz = pygame.transform.rotozoom(img, 0, sc)
    w = img_rz.get_width()
    h = img_rz.get_height()
    bg.blit(img_rz, [x - w / 2, y - h])


def draw_shadow(bg, x, y, siz):
    shadow = pygame.Surface([siz, siz / 4])
    shadow.fill(RED)
    shadow.set_colorkey(RED)  # Surface 투과색 설정
    shadow.set_alpha(128)  # Surface 투명도 설정
    pygame.draw.ellipse(shadow, BLACK, [0, 0, siz, siz / 4])
    bg.blit(shadow, [x - siz / 2, y - siz / 4])


def init_car():
    for i in range(1, CAR):
        car_x[i] = random.randint(50, 750)
        car_y[i] = random.randint(200, CMAX - 200)
        car_lr[i] = 0
        car_spd[i] = random.randint(100, 200)
    car_x[0] = 400
    car_y[0] = 0
    car_lr[0] = 0
    car_spd[0] = 0


def drive_car(key):  # 플레이어 차량 조작 및 제어
    if key[K_LEFT] == 1:
        if car_lr[0] > -3:
            car_lr[0] -= 1
        car_x[0] = car_x[0] + (car_lr[0] - 3) * car_spd[0] / 100 - 5
    elif key[K_RIGHT] == 1:
        if car_lr[0] < 3:
            car_lr[0] += 1
        car_x[0] = car_x[0] + (car_lr[0] + 3) * car_spd[0] / 100 + 5
    else:
        car_lr[0] = int(car_lr[0] * 0.9)

    if key[K_a] == 1:  # 악셀레이터
        car_spd[0] += 3
    elif key[K_z] == 1:  # 브레이크
        car_spd[0] -= 10
    else:
        car_spd[0] -= 0.25

    if car_spd[0] < 0:
        car_spd[0] = 0
    if car_spd[0] > 320:
        car_spd[0] = 320

    car_x[0] -= car_spd[0] * curve[int(car_y[0] + PLCAR_Y) % CMAX] / 50
    if car_x[0] < 0:
        car_x[0] = 0
        car_spd[0] *= 0.9
    if car_x[0] > 800:
        car_x[0] = 800
        car_spd[0] *= 0.9

    car_y[0] = car_y[0] + car_spd[0] / 100
    if car_y[0] > CMAX - 1:
        car_y[0] -= CMAX


def move_car(cs):  # COM 차량 제어
    for i in range(cs, CAR):
        if car_spd[i] < 100:
            car_spd[i] += 3
        if i == tmr % 120:
            car_lr[i] += random.choice([-1, 0, 1])
            if car_lr[i] < -3: car_lr[i] = -3
            if car_lr[i] > 3: car_lr[i] = 3
        car_x[i] = car_x[i] + car_lr[i] * car_spd[i] / 100
        if car_x[i] < 50:
            car_x[i] = 50
            car_lr[i] = int(car_lr[i] * 0.9)
        if car_x[i] > 750:
            car_x[i] = 750
            car_lr[i] = int(car_lr[i] * 0.9)
        car_y[i] += car_spd[i] / 100
        if car_y[i] > CMAX - 1:
            car_y[i] -= CMAX


def draw_text(scrn, txt, x, y, col, fnt):
    sur = fnt.render(txt, True, BLACK)
    x -= sur.get_width() / 2
    y -= sur.get_height() / 2
    scrn.blit(sur, [x + 2, y + 2])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])


def main():  # 메인 처리
    global tmr
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fnt_m = pygame.font.Font(None, 50)

    img_bg = pygame.image.load("image_pr/bg.png").convert()
    img_sea = pygame.image.load("image_pr/sea.png").convert_alpha()
    img_obj = [
        None,
        pygame.image.load("image_pr/board.png").convert_alpha(),
        pygame.image.load("image_pr/yashi.png").convert_alpha(),
        pygame.image.load("image_pr/yacht.png").convert_alpha()
    ]
    img_car = [
        pygame.image.load("image_pr/car00.png").convert_alpha(),
        pygame.image.load("image_pr/car01.png").convert_alpha(),
        pygame.image.load("image_pr/car02.png").convert_alpha(),
        pygame.image.load("image_pr/car03.png").convert_alpha(),
        pygame.image.load("image_pr/car04.png").convert_alpha(),
        pygame.image.load("image_pr/car05.png").convert_alpha(),
        pygame.image.load("image_pr/car06.png").convert_alpha(),
        pygame.image.load("image_pr/car10.png").convert_alpha(),
        pygame.image.load("image_pr/car11.png").convert_alpha(),
        pygame.image.load("image_pr/car12.png").convert_alpha(),
        pygame.image.load("image_pr/car13.png").convert_alpha(),
        pygame.image.load("image_pr/car14.png").convert_alpha(),
        pygame.image.load("image_pr/car15.png").convert_alpha(),
        pygame.image.load("image_pr/car16.png").convert_alpha(),
        pygame.image.load("image_pr/car20.png").convert_alpha(),
        pygame.image.load("image_pr/car21.png").convert_alpha(),
        pygame.image.load("image_pr/car22.png").convert_alpha(),
        pygame.image.load("image_pr/car23.png").convert_alpha(),
        pygame.image.load("image_pr/car24.png").convert_alpha(),
        pygame.image.load("image_pr/car25.png").convert_alpha(),
        pygame.image.load("image_pr/car26.png").convert_alpha()
    ]

    # 도로 판의 기본 형태 계산
    BOARD_W = [0] * BOARD
    BOARD_H = [0] * BOARD
    BOARD_UD = [0] * BOARD
    for i in range(BOARD):
        BOARD_W[i] = 10 + (BOARD - i) * (BOARD - i) / 12
        BOARD_H[i] = 3.4 * (BOARD - i) / BOARD
        BOARD_UD[i] = 2 * math.sin(math.radians(i * 1.5))

    make_course()
    init_car()

    vertical = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    screen = pygame.display.set_mode((800, 600), FULLSCREEN)
                if event.key == K_F2 or event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((800, 600))
        tmr += 1

        # 화면에 그릴 도로의 X 좌표와 높낮이 계산
        di = 0
        ud = 0
        board_x = [0] * BOARD
        board_ud = [0] * BOARD
        for i in range(BOARD):
            di += curve[int(car_y[0] + i) % CMAX]
            ud += updown[int(car_y[0] + i) % CMAX]
            board_x[i] = 400 - BOARD_W[i] * car_x[0] / 800 + di / 2
            board_ud[i] = ud / 30

        horizon = 400 + int(ud / 3)  # 지평선 좌표 계산
        sy = horizon  # 도로를 그리기 시작할 위치

        vertical = vertical - int(car_spd[0] * di / 8000)  # 베경 수직 위치
        if vertical < 0:
            vertical += 800
        if vertical >= 800:
            vertical -= 800

        # 필드 그리기
        screen.fill((0, 56, 255))  # 하늘 색상
        screen.blit(img_bg, [vertical - 800, horizon - 400])
        screen.blit(img_bg, [vertical, horizon - 400])
        screen.blit(img_sea, [board_x[BOARD - 1] - 780, sy])  # 가장 먼 바다

        # 그리기 데이터를 기초로 도로 그리기
        for i in range(BOARD - 1, 0, -1):
            ux = board_x[i]
            uy = sy - BOARD_UD[i] * board_ud[i]
            uw = BOARD_W[i]
            sy = sy + BOARD_H[i] * (600 - horizon) / 200
            bx = board_x[i - 1]
            by = sy - BOARD_UD[i - 1] * board_ud[i - 1]
            bw = BOARD_W[i - 1]
            col = (160, 160, 160)
            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

            if int(car_y[0] + i) % 10 <= 4:  # 좌우 노랑색 선
                pygame.draw.polygon(screen, YELLOW, [[ux, uy], [ux + uw * 0.02, uy], [bx + bw * 0.02, by], [bx, by]])
                pygame.draw.polygon(screen, YELLOW, [[ux + uw * 0.98, uy], [ux + uw, uy], [bx + bw, by], [bx + bw * 0.98, by]])
            if int(car_y[0] + i) % 20 <= 10:  # 흰색 선
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.24, uy], [ux + uw * 0.26, uy], [bx + bw * 0.26, by], [bx + bw * 0.24, by]])
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.49, uy], [ux + uw * 0.51, uy], [bx + bw * 0.51, by], [bx + bw * 0.49, by]])
                pygame.draw.polygon(screen, WHITE, [[ux + uw * 0.74, uy], [ux + uw * 0.76, uy], [bx + bw * 0.76, by], [bx + bw * 0.74, by]])

            scale = 1.5 * BOARD_W[i] / BOARD_W[0]
            obj_l = object_left[int(car_y[0] + i) % CMAX]  # 도로 왼쪽 물체
            if obj_l == 2:  # 야자 나무
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.05, uy, scale)
            if obj_l == 3:  # 요트
                draw_obj(screen, img_obj[obj_l], ux - uw * 0.5, uy, scale)
            if obj_l == 9:  # 바다
                screen.blit(img_sea, [ux - uw * 0.5 - 780, uy])
            obj_r = object_right[int(car_y[0] + i) % CMAX]  # 도로 오른쪽 물체
            if obj_r == 1:  # 간판
                draw_obj(screen, img_obj[obj_r], ux + uw * 1.3, uy, scale)

            for c in range(1, CAR):  # COM 차량
                if int(car_y[c]) % CMAX == int(car_y[0] + i) % CMAX:
                    lr = int(4 * (car_x[0] - car_x[c]) / 800)  # 플레이어가 보는 COM 차량의 방향
                    if lr < -3: lr = -3
                    if lr > 3: lr = 3
                    draw_obj(screen, img_car[(c % 3) * 7 + 3 + lr], ux + car_x[c] * BOARD_W[i] / 800, uy, 0.05 + BOARD_W[i] / BOARD_W[0])

            if i == PLCAR_Y:  # 플레이어 차량
                draw_shadow(screen, ux + car_x[0] * BOARD_W[i] / 800, uy, 200 * BOARD_W[i] / BOARD_W[0])
                draw_obj(screen, img_car[3 + car_lr[0]], ux + car_x[0] * BOARD_W[i] / 800, uy, 0.05 + BOARD_W[i] / BOARD_W[0])

        draw_text(screen, str(int(car_spd[0])) + "km/h", 680, 30, RED, fnt_m)

        key = pygame.key.get_pressed()
        drive_car(key)
        move_car(1)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
