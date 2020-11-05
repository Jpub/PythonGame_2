import tkinter

def mouse_click(e):
    px = e.x
    py = e.y
    print("마우스 포인터 좌표: ({},{})".format(px, py))
    mx = int(px / 48)
    my = int(py / 48)
    if 0 <= mx and mx <= 6 and 0 <= my and my <= 4:
        n = map_data[my][mx]
        print("여기에 있는 맵 칩은 " + CHIP_NAME[n])

root = tkinter.Tk()
root.title("맵 데이터")
canvas = tkinter.Canvas(width=336, height=240)
canvas.pack()
canvas.bind("<Button>", mouse_click)
CHIP_NAME = ["풀", "꽃", "숲", "바다"]
img = [
    tkinter.PhotoImage(file="chip0.png"),
    tkinter.PhotoImage(file="chip1.png"),
    tkinter.PhotoImage(file="chip2.png"),
    tkinter.PhotoImage(file="chip3.png")
]
map_data = [
    [0, 1, 0, 2, 2, 2, 2],
    [3, 0, 0, 0, 2, 2, 2],
    [3, 0, 0, 1, 0, 0, 0],
    [3, 3, 0, 0, 0, 0, 1],
    [3, 3, 3, 3, 0, 0, 0]
]
for y in range(5):
    for x in range(7):
        canvas.create_image(x * 48 + 24, y * 48 + 24, image=img[map_data[y][x]])
root.mainloop()
