import tkinter

chip = 0
map_data = []
for i in range(9):
    map_data.append([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])

def draw_map():
    cvs_bg.delete("BG")
    for y in range(9):
        for x in range(12):
            cvs_bg.create_image(60 * x + 30, 60 * y + 30, image=img[map_data[y][x]], tag="BG")

def set_map(e):
    x = int(e.x / 60)
    y = int(e.y / 60)
    if 0 <= x and x <= 11 and 0 <= y and y <= 8:
        map_data[y][x] = chip
        draw_map()

def draw_chip():
    cvs_chip.delete("CHIP")
    for i in range(len(img)):
        cvs_chip.create_image(30, 30 + i * 60, image=img[i], tag="CHIP")
    cvs_chip.create_rectangle(4, 4 + 60 * chip, 57, 57 + 60 * chip, outline="red", width=3, tag="CHIP")

def select_chip(e):
    global chip
    y = int(e.y / 60)
    if 0 <= y and y < len(img):
        chip = y
        draw_chip()

root = tkinter.Tk()
root.geometry("820x560")
root.title("맵 에디터")
cvs_bg = tkinter.Canvas(width=720, height=540, bg="white")
cvs_bg.place(x=10, y=10)
cvs_bg.bind("<Button-1>", set_map)
cvs_bg.bind("<B1-Motion>", set_map)
cvs_chip = tkinter.Canvas(width=60, height=540, bg="black")
cvs_chip.place(x=740, y=10)
cvs_chip.bind("<Button-1>", select_chip)
img = [
    tkinter.PhotoImage(file="image_penpen/chip00.png"),
    tkinter.PhotoImage(file="image_penpen/chip01.png"),
    tkinter.PhotoImage(file="image_penpen/chip02.png"),
    tkinter.PhotoImage(file="image_penpen/chip03.png")
]
draw_map()
draw_chip()
root.mainloop()
