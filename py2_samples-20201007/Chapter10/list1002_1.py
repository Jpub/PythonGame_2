import pygame
import sys
import math
from pygame.locals import *

BOARD = 120
CMAX = BOARD * 4
curve = [0] * CMAX


def make_course():
    for i in range(360):
        curve[BOARD + i] = int(5 * math.sin(math.radians(i)))


def main():  # 메인 처리
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    img_bg = pygame.image.load("image_pr/bg.png").convert()

    # 도로 판의 기본 형태 계산
    BOARD_W = [0] * BOARD
    BOARD_H = [0] * BOARD
    for i in range(BOARD):
        BOARD_W[i] = 10 + (BOARD - i) * (BOARD - i) / 12
        BOARD_H[i] = 3.4 * (BOARD - i) / BOARD

    make_course()

    car_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[K_UP] == 1:
            car_y = (car_y + 1) % CMAX

        # 화면에 그릴 도로 X 좌표 계산
        di = 0
        board_x = [0] * BOARD
        for i in range(BOARD):
            di += curve[(car_y + i) % CMAX]
            board_x[i] = 400 - BOARD_W[i] / 2 + di / 2

        sy = 400  # 도로를 그리기 시작할 위치

        screen.blit(img_bg, [0, 0])

        # 그리기 데이터를 기초로 도로 그리기
        for i in range(BOARD - 1, 0, -1):
            ux = board_x[i]
            uy = sy
            uw = BOARD_W[i]
            sy = sy + BOARD_H[i]
            bx = board_x[i - 1]
            by = sy
            bw = BOARD_W[i - 1]
            col = (160, 160, 160)
            if (car_y + i) % 12 == 0:
                col = (255, 255, 255)
            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
