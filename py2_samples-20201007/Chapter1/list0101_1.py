import tkinter

root = tkinter.Tk()
root.geometry("400x200")
root.title("파이썬에서 GUI 다루기")
label = tkinter.Label(root, text="게임 개발 첫 걸음", font=("Times New Roman", 20))
label.place(x=80, y=60)
root.mainloop()
