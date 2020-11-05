import tkinter

root = tkinter.Tk()
root.title("도로 그리기")
canvas = tkinter.Canvas(width=800, height=600, bg="blue")
canvas.pack()

canvas.create_rectangle(0, 300, 800, 600, fill="green")

BORD_COL = ["white", "silver", "gray"]
h = 2
y = 300
for i in range(1, 24):
    uw = i * i * 1.5
    ux = 400 - uw / 2
    bw = (i + 1) * (i + 1) * 1.5
    bx = 400 - bw / 2
    col = BORD_COL[i % 3]
    canvas.create_polygon(ux, y, ux + uw, y, bx + bw, y + h, bx, y + h, fill=col)
    y = y + h
    h = h + 1

root.mainloop()
