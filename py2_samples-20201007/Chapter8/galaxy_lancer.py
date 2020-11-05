import pygame
import sys
import math
import random
from pygame.locals import *

BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)

# 이미지 로딩
img_galaxy = pygame.image.load("image_gl/galaxy.png")
img_sship = [
    pygame.image.load("image_gl/starship.png"),
    pygame.image.load("image_gl/starship_l.png"),
    pygame.image.load("image_gl/starship_r.png"),
    pygame.image.load("image_gl/starship_burner.png")
]
img_weapon = pygame.image.load("image_gl/bullet.png")
img_shield = pygame.image.load("image_gl/shield.png")
img_enemy = [
    pygame.image.load("image_gl/enemy0.png"),
    pygame.image.load("image_gl/enemy1.png"),
    pygame.image.load("image_gl/enemy2.png"),
    pygame.image.load("image_gl/enemy3.png"),
    pygame.image.load("image_gl/enemy4.png"),
    pygame.image.load("image_gl/enemy_boss.png"),
    pygame.image.load("image_gl/enemy_boss_f.png")
]
img_explode = [
    None,
    pygame.image.load("image_gl/explosion1.png"),
    pygame.image.load("image_gl/explosion2.png"),
    pygame.image.load("image_gl/explosion3.png"),
    pygame.image.load("image_gl/explosion4.png"),
    pygame.image.load("image_gl/explosion5.png")
]
img_title = [
    pygame.image.load("image_gl/nebula.png"),
    pygame.image.load("image_gl/logo.png")
]

# SE 로딩 변수
se_barrage = None
se_damage = None
se_explosion = None
se_shot = None

idx = 0
tmr = 0
score = 0
hisco = 10000
new_record = False
bg_y = 0

ss_x = 0
ss_y = 0
ss_d = 0
ss_shield = 0
ss_muteki = 0
key_spc = 0
key_z = 0

MISSILE_MAX = 200
msl_no = 0
msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX
msl_y = [0] * MISSILE_MAX
msl_a = [0] * MISSILE_MAX

ENEMY_MAX = 100
emy_no = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX
emy_type = [0] * ENEMY_MAX
emy_speed = [0] * ENEMY_MAX
emy_shield = [0] * ENEMY_MAX
emy_count = [0] * ENEMY_MAX

EMY_BULLET = 0
EMY_ZAKO = 1
EMY_BOSS = 5
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040

EFFECT_MAX = 100
eff_no = 0
eff_p = [0] * EFFECT_MAX
eff_x = [0] * EFFECT_MAX
eff_y = [0] * EFFECT_MAX


def get_dis(x1, y1, x2, y2):  # 두 점 사이 거리 계산
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def draw_text(scrn, txt, x, y, siz, col):  # 입체적인 문자 표시
    fnt = pygame.font.Font(None, siz)
    cr = int(col[0] / 2)
    cg = int(col[1] / 2)
    cb = int(col[2] / 2)
    sur = fnt.render(txt, True, (cr, cg, cb))
    x = x - sur.get_width() / 2
    y = y - sur.get_height() / 2
    scrn.blit(sur, [x + 1, y + 1])
    cr = col[0] + 128
    if cr > 255: cr = 255
    cg = col[1] + 128
    if cg > 255: cg = 255
    cb = col[2] + 128
    if cb > 255: cb = 255
    sur = fnt.render(txt, True, (cr, cg, cb))
    scrn.blit(sur, [x - 1, y - 1])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])


def move_starship(scrn, key):  # 플레이어 기체 이동
    global idx, tmr, ss_x, ss_y, ss_d, ss_shield, ss_muteki, key_spc, key_z
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
    key_spc = (key_spc + 1) * key[K_SPACE]
    if key_spc % 5 == 1:
        set_missile(0)
        se_shot.play()
    key_z = (key_z + 1) * key[K_z]
    if key_z == 1 and ss_shield > 10:
        set_missile(10)
        ss_shield = ss_shield - 10
        se_barrage.play()

    if ss_muteki % 2 == 0:
        scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2])
        scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48])

    if ss_muteki > 0:
        ss_muteki = ss_muteki - 1
        return
    elif idx == 1:
        for i in range(ENEMY_MAX):  # 적 기체와 히트 체크
            if emy_f[i] == True:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w + h) / 4 + (74 + 96) / 4)
                if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r * r:
                    set_effect(ss_x, ss_y)
                    ss_shield = ss_shield - 10
                    if ss_shield <= 0:
                        ss_shield = 0
                        idx = 2
                        tmr = 0
                    if ss_muteki == 0:
                        ss_muteki = 60
                        se_damage.play()
                    if emy_type[i] < EMY_BOSS:
                        emy_f[i] = False


def set_missile(typ):  # 플레이어 기체 발사 탄환 설정
    global msl_no
    if typ == 0:  # 단발
        msl_f[msl_no] = True
        msl_x[msl_no] = ss_x
        msl_y[msl_no] = ss_y - 50
        msl_a[msl_no] = 270
        msl_no = (msl_no + 1) % MISSILE_MAX
    if typ == 10:  # 탄막
        for a in range(160, 390, 10):
            msl_f[msl_no] = True
            msl_x[msl_no] = ss_x
            msl_y[msl_no] = ss_y - 50
            msl_a[msl_no] = a
            msl_no = (msl_no + 1) % MISSILE_MAX


def move_missile(scrn):  # 탄환 이동
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i]))
            msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i]))
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - msl_a[i], 1.0)
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False


def bring_enemy():  # 적 기체 등장
    sec = tmr / 30
    if 0 < sec and sec < 25:  # 시작 후 25초 간
        if tmr % 15 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1
    if 30 < sec and sec < 55:  # 30~55초
        if tmr % 10 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1)  # 적 2
    if 60 < sec and sec < 85:  # 60~85초
        if tmr % 15 == 0:
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)  # 적 3
    if 90 < sec and sec < 115:  # 90~115초
        if tmr % 20 == 0:
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)  # 적 4
    if 120 < sec and sec < 145:  # 120~145초, 2종류
        if tmr % 20 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)  # 적 3
    if 150 < sec and sec < 175:  # 150~175초, 2종류
        if tmr % 20 == 0:
            set_enemy(random.randint(20, 940), LINE_B, 270, EMY_ZAKO, 8, 1)  # 적 1 아래에서 위로
            set_enemy(random.randint(20, 940), LINE_T, random.randint(70, 110), EMY_ZAKO + 1, 12, 1)  # 적 2
    if 180 < sec and sec < 205:  # 180~205초, 2종류
        if tmr % 20 == 0:
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)  # 적 3
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)  # 적 4
    if 210 < sec and sec < 235:  # 210~235초, 2종류
        if tmr % 20 == 0:
            set_enemy(LINE_L, random.randint(40, 680), 0, EMY_ZAKO, 12, 1)  # 적 1
            set_enemy(LINE_R, random.randint(40, 680), 180, EMY_ZAKO + 1, 18, 1)  # 적 2
    if 240 < sec and sec < 265:  # 240~265초, 총공격
        if tmr % 30 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)  # 적 1
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1)  # 적 2
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)  # 적 3
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)  # 적 4

    if tmr == 30 * 270:  # 보스 출현
        set_enemy(480, -210, 90, EMY_BOSS, 4, 200)


def set_enemy(x, y, a, ty, sp, sh):  # 적 기체 설정
    global emy_no
    while True:
        if emy_f[emy_no] == False:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            emy_shield[emy_no] = sh
            emy_count[emy_no] = 0
            break
        emy_no = (emy_no + 1) % ENEMY_MAX


def move_enemy(scrn):  # 적 기체 이동
    global idx, tmr, score, hisco, new_record, ss_shield
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90 - emy_a[i]
            png = emy_type[i]
            if emy_type[i] < EMY_BOSS:  # 적 일반 기체 이동
                emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
                emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))
                if emy_type[i] == 4:  # 진행 방향을 변경하는 적
                    emy_count[i] = emy_count[i] + 1
                    ang = emy_count[i] * 10
                    if emy_y[i] > 240 and emy_a[i] == 90:
                        emy_a[i] = random.choice([50, 70, 110, 130])
                        set_enemy(emy_x[i], emy_y[i], 90, EMY_BULLET, 6, 0)
                if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                    emy_f[i] = False
            else:  # 보스 기체
                if emy_count[i] == 0:
                    emy_y[i] = emy_y[i] + 2
                    if emy_y[i] >= 200:
                        emy_count[i] = 1
                elif emy_count[i] == 1:
                    emy_x[i] = emy_x[i] - emy_speed[i]
                    if emy_x[i] < 200:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0)
                        emy_count[i] = 2
                else:
                    emy_x[i] = emy_x[i] + emy_speed[i]
                    if emy_x[i] > 760:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0)
                        emy_count[i] = 1
                if emy_shield[i] < 100 and tmr % 30 == 0:
                    set_enemy(emy_x[i], emy_y[i] + 80, random.randint(60, 120), EMY_BULLET, 6, 0)

            if emy_type[i] != EMY_BULLET:  # 플레이어 기체 발사 탄환과 히트 체크
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w + h) / 4) + 12
                er = int((w + h) / 4)
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r:
                        msl_f[n] = False
                        set_effect(emy_x[i] + random.randint(-er, er), emy_y[i] + random.randint(-er, er))
                        if emy_type[i] == EMY_BOSS:  # 보스 기체 깜빡임 처리
                            png = emy_type[i] + 1
                        emy_shield[i] = emy_shield[i] - 1
                        score = score + 100
                        if score > hisco:
                            hisco = score
                            new_record = True
                        if emy_shield[i] == 0:
                            emy_f[i] = False
                            if ss_shield < 100:
                                ss_shield = ss_shield + 1
                            if emy_type[i] == EMY_BOSS and idx == 1:  # 보스를 격추시키면 클리어
                                idx = 3
                                tmr = 0
                                for j in range(10):
                                    set_effect(emy_x[i] + random.randint(-er, er), emy_y[i] + random.randint(-er, er))
                                se_explosion.play()

            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2])


def set_effect(x, y):  # 폭발 설정
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % EFFECT_MAX


def draw_effect(scrn):  # 폭발 연출
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48])
            eff_p[i] = eff_p[i] + 1
            if eff_p[i] == 6:
                eff_p[i] = 0


def main():  # 메인 루프
    global idx, tmr, score, new_record, bg_y, ss_x, ss_y, ss_d, ss_shield, ss_muteki
    global se_barrage, se_damage, se_explosion, se_shot

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()
    se_barrage = pygame.mixer.Sound("sound_gl/barrage.ogg")
    se_damage = pygame.mixer.Sound("sound_gl/damage.ogg")
    se_explosion = pygame.mixer.Sound("sound_gl/explosion.ogg")
    se_shot = pygame.mixer.Sound("sound_gl/shot.ogg")

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

        if idx == 0:  # 타이틀
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr % 360, 1.0)
            screen.blit(img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2])
            screen.blit(img_title[1], [70, 160])
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                score = 0
                new_record = False
                ss_x = 480
                ss_y = 600
                ss_d = 0
                ss_shield = 100
                ss_muteki = 0
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(MISSILE_MAX):
                    msl_f[i] = False
                pygame.mixer.music.load("sound_gl/bgm.ogg")
                pygame.mixer.music.play(-1)

        if idx == 1:  # 게임 플레이 중
            move_starship(screen, key)
            move_missile(screen)
            bring_enemy()
            move_enemy(screen)

        if idx == 2:  # 게임 오버
            move_missile(screen)
            move_enemy(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr <= 90:
                if tmr % 5 == 0:
                    set_effect(ss_x + random.randint(-60, 60), ss_y + random.randint(-60, 60))
                if tmr % 10 == 0:
                    se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load("sound_gl/gameover.ogg")
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_text(screen, "GAME OVER", 480, 300, 80, RED)
                if new_record == True:
                    draw_text(screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN)
            if tmr == 400:
                idx = 0
                tmr = 0

        if idx == 3:  # 게임 클리어
            move_starship(screen, key)
            move_missile(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr < 30 and tmr % 2 == 0:
                pygame.draw.rect(screen, (192, 0, 0), [0, 0, 960, 720])
            if tmr == 120:
                pygame.mixer.music.load("sound_gl/gameclear.ogg")
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER)
                if new_record == True:
                    draw_text(screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN)
            if tmr == 400:
                idx = 0
                tmr = 0

        draw_effect(screen)  # 폭발 연출
        draw_text(screen, "SCORE " + str(score), 200, 30, 50, SILVER)
        draw_text(screen, "HISCORE " + str(hisco), 760, 30, 50, CYAN)
        if idx != 0:  # 실드 표시
            screen.blit(img_shield, [40, 680])
            pygame.draw.rect(screen, (64, 32, 32), [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 12])

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
