import tkinter
import math

root = tkinter.Tk()
root.title("삼각함수를 활용한 선 그리기")
canvas = tkinter.Canvas(width=400, height=400, bg="white")
canvas.pack()
for d in range(0, 90, 10):
    a = math.radians(d)
    x = 300 * math.cos(a)
    y = 300 * math.sin(a)
    canvas.create_line(0, 0, x, y, fill="blue")
root.mainloop()
