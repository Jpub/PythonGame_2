import pygame
import sys

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/galaxy.png")
img_sship = pygame.image.load("image_gl/starship.png")

bg_y = 0

ss_x = 480
ss_y = 360


def move_starship(scrn, key):  # 플레이어 기체 이동
    global ss_x, ss_y
    if key[pygame.K_UP] == 1:
        ss_y = ss_y - 20
        if ss_y < 80:
            ss_y = 80
    if key[pygame.K_DOWN] == 1:
        ss_y = ss_y + 20
        if ss_y > 640:
            ss_y = 640
    if key[pygame.K_LEFT] == 1:
        ss_x = ss_x - 20
        if ss_x < 40:
            ss_x = 40
    if key[pygame.K_RIGHT] == 1:
        ss_x = ss_x + 20
        if ss_x > 920:
            ss_x = 920
    scrn.blit(img_sship, [ss_x - 37, ss_y - 48])


def main():  # 메인 루프
    global bg_y

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen, key)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
