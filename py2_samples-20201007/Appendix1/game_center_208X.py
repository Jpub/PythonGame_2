import tkinter
import penpen_pygame
import galaxy_lancer_gp
import python_racer

def key_down(e):
    key = e.keysym
    if key == "1":
        penpen_pygame.main()
    if key == "2":
        galaxy_lancer_gp.main()
    if key == "3":
        python_racer.main()

root = tkinter.Tk()
root.title("Game Center 2080's")
root.resizable(False, False)
root.bind("<KeyPress>", key_down)
canvas = tkinter.Canvas(width=800, height=800)
canvas.pack()
img = tkinter.PhotoImage(file="gc2080.png")
canvas.create_image(400, 400, image=img)
root.mainloop()
