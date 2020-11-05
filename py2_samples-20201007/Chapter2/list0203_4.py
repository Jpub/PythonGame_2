import tkinter
import math

root = tkinter.Tk()
root.title("삼각함수를 활용한 도형 그리기")
canvas = tkinter.Canvas(width=600, height=600, bg="black")
canvas.pack()

COL = ["greenyellow", "limegreen", "aquamarine", "cyan", "deepskyblue", "blue", "blueviolet", "violet"]
for d in range(0, 360):
    x = 250 * math.cos(math.radians(d))
    y = 250 * math.sin(math.radians(d))
    canvas.create_line(300, 300, 300 + x, 300 + y, fill=COL[d % 8], width=2)
root.mainloop()
