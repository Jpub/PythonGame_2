import tkinter

# 키 입력
key = ""
koff = False
def key_down(e):
    global key, koff
    key = e.keysym
    koff = False

def key_up(e):
    global koff
    koff = True

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

pen_x = 90
pen_y = 90

map_data = [
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 2, 3, 3, 2, 1, 1, 2, 3, 3, 2, 0],
    [0, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 0],
    [0, 3, 1, 1, 3, 0, 0, 3, 1, 1, 3, 0],
    [0, 3, 2, 2, 3, 0, 0, 3, 2, 2, 3, 0],
    [0, 3, 0, 0, 3, 1, 1, 3, 0, 0, 3, 0],
    [0, 3, 1, 1, 3, 3, 3, 3, 1, 1, 3, 0],
    [0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def draw_screen():  # 게임 화면 그리기
    canvas.delete("SCREEN")
    for y in range(9):
        for x in range(12):
            canvas.create_image(x * 60 + 30, y * 60 + 30, image=img_bg[map_data[y][x]], tag="SCREEN")
    canvas.create_image(pen_x, pen_y, image=img_pen, tag="SCREEN")


def check_wall(cx, cy, di):  # 각 방향에 벽 존재 여부 확인
    chk = False
    if di == DIR_UP:
        mx = int(cx / 60)
        my = int((cy - 60) / 60)
        if map_data[my][mx] <= 1:
            chk = True
    if di == DIR_DOWN:
        mx = int(cx / 60)
        my = int((cy + 60) / 60)
        if map_data[my][mx] <= 1:
            chk = True
    if di == DIR_LEFT:
        mx = int((cx - 60) / 60)
        my = int(cy / 60)
        if map_data[my][mx] <= 1:
            chk = True
    if di == DIR_RIGHT:
        mx = int((cx + 60) / 60)
        my = int(cy / 60)
        if map_data[my][mx] <= 1:
            chk = True
    return chk


def move_penpen():  # 펜펜 움직이기
    global pen_x, pen_y
    if key == "Up":
        if check_wall(pen_x, pen_y, DIR_UP) == False:
            pen_y = pen_y - 60
    if key == "Down":
        if check_wall(pen_x, pen_y, DIR_DOWN) == False:
            pen_y = pen_y + 60
    if key == "Left":
        if check_wall(pen_x, pen_y, DIR_LEFT) == False:
            pen_x = pen_x - 60
    if key == "Right":
        if check_wall(pen_x, pen_y, DIR_RIGHT) == False:
            pen_x = pen_x + 60


def main():  # 메인 루프
    global key, koff
    draw_screen()
    move_penpen()
    if koff == True:
        key = ""
        koff = False
    root.after(300, main)


root = tkinter.Tk()

img_bg = [
    tkinter.PhotoImage(file="image_penpen/chip00.png"),
    tkinter.PhotoImage(file="image_penpen/chip01.png"),
    tkinter.PhotoImage(file="image_penpen/chip02.png"),
    tkinter.PhotoImage(file="image_penpen/chip03.png")
]
img_pen = tkinter.PhotoImage(file="image_penpen/pen03.png")

root.title("아슬아슬 펭귄 미로")
root.resizable(False, False)
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=720, height=540)
canvas.pack()
main()
root.mainloop()
