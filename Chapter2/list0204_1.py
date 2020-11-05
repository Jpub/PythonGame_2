import tkinter

fnt1 = ("Times New Roman", 20)
fnt2 = ("Times New Roman", 40)
index = 0
timer = 0

key = ""
def key_down(e):
    global key
    key = e.keysym

def main():
    global index, timer
    canvas.delete("STATUS")
    timer = timer + 1
    canvas.create_text(200, 30, text="index " + str(index), fill="white", font=fnt1, tag="STATUS")
    canvas.create_text(400, 30, text="timer " + str(timer), fill="cyan", font=fnt1, tag="STATUS")

    if index == 0:
        if timer == 1:
            canvas.create_text(300, 150, text="타이틀", fill="white", font=fnt2, tag="TITLE")
            canvas.create_text(300, 300, text="Press[SPACE]Key", fill="lime", font=fnt1, tag="TITLE")
        if key == "space":
            canvas.delete("TITLE")
            canvas.create_rectangle(0, 0, 600, 400, fill="blue", tag="GAME")
            canvas.create_text(300, 150, text="게임 중", fill="white", font=fnt2, tag="GAME")
            canvas.create_text(300, 300, text="[E] 종료", fill="yellow", font=fnt1, tag="GAME")
            index = 1
            timer = 0

    if index == 1:
        if key == "e":
            canvas.delete("GAME")
            canvas.create_rectangle(0, 0, 600, 400, fill="maroon", tag="OVER")
            canvas.create_text(300, 150, text="GAME OVER", fill="red", font=fnt2, tag="OVER")
            index = 2
            timer = 0

    if index == 2:
        if timer == 30:
            canvas.delete("OVER")
            index = 0
            timer = 0

    root.after(100, main)

root = tkinter.Tk()
root.title("인덱스와 타이머")
root.bind("<KeyPress>", key_down)
canvas = tkinter.Canvas(width=600, height=400, bg="black")
canvas.pack()
main()
root.mainloop()
