import tkinter as tk
from PIL import Image, ImageTk 

root = tk.Tk()
root.title("People Counter Vision System")

root.geometry("1920x1080")
#root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
canvas.pack()

root.mainloop()
