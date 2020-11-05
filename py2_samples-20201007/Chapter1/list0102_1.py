import tkinter
import datetime

def time_now():
    d = datetime.datetime.now()
    t = "{0}:{1}:{2}".format(d.hour, d.minute, d.second)
    label["text"] = t
    root.after(1000, time_now)

root = tkinter.Tk()
root.geometry("400x100")
root.title("간이 계산")
label = tkinter.Label(font=("Times New Roman", 60))
label.pack()
time_now()
root.mainloop()
