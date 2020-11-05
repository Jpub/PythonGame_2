import tkinter

def key_down(e):
    key = e.keysym
    if key == "Up":
        draw_road(0)
    if key == "Left":
        draw_road(-10)
    if key == "Right":
        draw_road(10)

BORD_COL = ["white", "silver", "gray"]
def draw_road(di):
    canvas.delete("ROAD")
    h = 24
    y = 600 - h
    for i in range(23, 0, -1):
        uw = (i - 1) * (i - 1) * 1.5
        ux = 400 - uw / 2 + di * (23 - (i - 1))
        bw = i * i * 1.5
        bx = 400 - bw / 2 + di * (23 - i)
        col = BORD_COL[i % 3]
        canvas.create_polygon(ux, y, ux + uw, y, bx + bw, y + h, bx, y + h, fill=col, tag="ROAD")
        h = h - 1
        y = y - h

root = tkinter.Tk()
root.title("도로 그리기")
root.bind("<Key>", key_down)
canvas = tkinter.Canvas(width=800, height=600, bg="blue")
canvas.pack()
canvas.create_rectangle(0, 300, 800, 600, fill="green")
canvas.create_text(400, 100, text="위쪽, 왼쪽, 오른쪽 방향키를 눌러 주십시오", fill="white")
root.mainloop()
