import tkinter
import math

def hit_check_circle():
    dis = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    if dis <= r1 + r2:
        return True
    return False

def mouse_move(e):
    global x1, y1
    x1 = e.x
    y1 = e.y
    col = "green"
    if hit_check_circle() == True:
        col = "lime"
    canvas.delete("CIR1")
    canvas.create_oval(x1 - r1, y1 - r1, x1 + r1, y1 + r1, fill=col, tag="CIR1")

root = tkinter.Tk()
root.title("원을 사용한 히트 체크")
canvas = tkinter.Canvas(width=600, height=400, bg="white")
canvas.pack()
canvas.bind("<Motion>", mouse_move)

x1 = 50
y1 = 50
r1 = 40
canvas.create_oval(x1 - r1, y1 - r1, x1 + r1, y1 + r1, fill="green", tag="CIR1")

x2 = 300
y2 = 200
r2 = 80
canvas.create_oval(x2 - r2, y2 - r2, x2 + r2, y2 + r2, fill="orange")

root.mainloop()
