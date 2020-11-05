import pygame
import sys
from pygame.locals import *

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/galaxy.png")
img_sship = [
    pygame.image.load("image_gl/starship.png"),
    pygame.image.load("image_gl/starship_l.png"),
    pygame.image.load("image_gl/starship_r.png"),
    pygame.image.load("image_gl/starship_burner.png")
]
img_weapon = pygame.image.load("image_gl/bullet.png")

tmr = 0
bg_y = 0

ss_x = 480
ss_y = 360
ss_d = 0

msl_f = False
msl_x = 0
msl_y = 0


def move_starship(scrn, key):  # 플레이어 기체 이동
    global ss_x, ss_y, ss_d
    ss_d = 0
    if key[K_UP] == 1:
        ss_y = ss_y - 20
        if ss_y < 80:
            ss_y = 80
    if key[K_DOWN] == 1:
        ss_y = ss_y + 20
        if ss_y > 640:
            ss_y = 640
    if key[K_LEFT] == 1:
        ss_d = 1
        ss_x = ss_x - 20
        if ss_x < 40:
            ss_x = 40
    if key[K_RIGHT] == 1:
        ss_d = 2
        ss_x = ss_x + 20
        if ss_x > 920:
            ss_x = 920
    if key[K_SPACE] == 1:
        set_missile()
    scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2])
    scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48])


def set_missile():  # 플레이어 기체 발사 탄환 설정
    global msl_f, msl_x, msl_y
    if msl_f == False:
        msl_f = True
        msl_x = ss_x
        msl_y = ss_y - 50


def move_missile(scrn):  # 탄환 이동
    global msl_f, msl_y
    if msl_f == True:
        msl_y = msl_y - 36
        scrn.blit(img_weapon, [msl_x - 10, msl_y - 32])
        if msl_y < 0:
            msl_f = False


def main():  # 메인 루프
    global tmr, bg_y

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    screen = pygame.display.set_mode((960, 720), FULLSCREEN)
                if event.key == K_F2 or event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen, key)
        move_missile(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
