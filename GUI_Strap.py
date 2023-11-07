import tkinter as tk
from PIL import Image, ImageTk 
import threading
import variables

def loop_function():

    if variables.Variable_strap_A[0] == 1:
        Correct_function()

    elif variables.Variable_strap_A[0] == 2:
        Wrong_function()

    elif variables.Variable_strap_B[0] == 1:
         Correct_function()
    
    elif variables.Variable_strap_B[0] == 2:
         Wrong_function()

    elif variables.Variable_strap_C[0] == 1:
        Correct_function()
    
    elif variables.Variable_strap_C[0] == 2:
        Wrong_function()

    else:
        Waiting_function()
        
    if variables.Stop_program[0] == 1:
        canvas.after(100, loop_function)
    else:
        canvas.configure(bg="white")
        button_Turn_off.configure(bg="white")
        button_back.destroy()
        try: canvas.delete(Strap_a_image) 
        except: pass
        try: canvas.delete(Strap_b_image) 
        except: pass
        try: canvas.delete(Strap_c_image)
        except: pass
        try: canvas.delete(Waiting)
        except: pass
        try: canvas.delete(Correct)
        except: pass
        try: canvas.delete(Wrong)
        except: pass

def strap_a_action():
    global Strap_a_image
    Strap_a_image = canvas.create_image(512, 120, image=img_a)
    variables.Stop_program[0] = 1
    variables.Strap_A_detection[0] = 1
    destroy_principal()
    loop_function()

def strap_b_action():
    global Strap_b_image
    Strap_b_image = canvas.create_image(512, 120, image=img_b)
    variables.Stop_program[0] = 1
    variables.Strap_B_detection[0] = 1
    destroy_principal()
    loop_function()

def strap_c_action():
    global Strap_c_image
    Strap_c_image = canvas.create_image(512, 120, image=img_c)
    variables.Stop_program[0] = 1
    variables.Strap_C_detection[0] = 1
    destroy_principal()
    loop_function()

def Waiting_function():
    global Waiting
    try: canvas.delete(Correct)
    except: pass
    try: canvas.delete(Wrong)
    except: pass
    try: canvas.delete(Waiting)
    except: pass
    Waiting = canvas.create_text(512, 300, text="Waiting for detections...", font=("Helvetica", 40), fill="black")
    canvas.configure(bg="white")
    button_back.configure(bg="white")
    button_Turn_off.configure(bg="white")

def Correct_function():
    global Correct
    try: canvas.delete(Waiting)
    except: pass
    try: canvas.delete(Wrong)
    except: pass
    try: canvas.delete(Correct)
    except: pass

    Correct = canvas.create_text(512, 300, text="Correct Strap", font=("Helvetica", 40), fill="black")
    canvas.configure(bg="green")
    button_back.configure(bg="green")
    button_Turn_off.configure(bg="green")

def Wrong_function():
    global Wrong
    try: canvas.delete(Waiting)
    except: pass
    try: canvas.delete(Correct)
    except: pass
    try: canvas.delete(Wrong)
    except: pass

    Wrong = canvas.create_text(512, 300, text="Wrong Strap", font=("Helvetica", 40), fill="black")
    canvas.configure(bg="red")
    button_back.configure(bg="red")
    button_Turn_off.configure(bg="red")

def destroy_principal():
    global button_back
    button_a.destroy()
    canvas.delete(text_a)
    button_b.destroy()
    canvas.delete(text_b)
    button_c.destroy()
    canvas.delete(text_c)
    canvas.delete(title)
    button_back = tk.Button(canvas, image=back, command=back_action,  bg="white", borderwidth=0, relief="flat")
    button_back.place(x = 15, y = 15, height=50, width=50)

def back_action():
    variables.Strap_A_detection[0] = 0
    variables.Strap_B_detection[0] = 0
    variables.Strap_C_detection[0] = 0
    variables.Stop_program[0] = 0
    index()

def turn_off_action():
    variables.Shut_down[0] = 1
    root.destroy()

def index():
    global button_a, button_b, button_c, text_a, text_b, text_c, title, button_back, button_Turn_off
    canvas.configure(bg="white")
    title = canvas.create_text(512, 50, text="Strap Visual System", font=("Helvetica", 40), fill="black")
    button_a = tk.Button(canvas, image=img_a, command=strap_a_action, bg="white", borderwidth=0, relief="flat")
    button_b = tk.Button(canvas, image=img_b, command=strap_b_action, bg="white", borderwidth=0, relief="flat")
    button_c = tk.Button(canvas, image=img_c, command=strap_c_action, bg="white", borderwidth=0, relief="flat")
    button_Turn_off = tk.Button(canvas, image=Turn_off, command=turn_off_action, bg="white", borderwidth=0, relief="flat")  
    
    text_a = canvas.create_text(200, 430, text="Strap A", font=("Helvetica", 24), fill="black")
    button_a.place(x = 106, y = 200, height=200, width=200)

    text_b = canvas.create_text(512, 430, text="Strap B", font=("Helvetica", 24), fill="black")
    button_b.place(x = 412, y = 200, height=200, width=200)
    
    text_c = canvas.create_text(818, 430, text="Strap C", font=("Helvetica", 24), fill="black")
    button_c.place(x = 718, y = 200, height=200, width=200)

    button_Turn_off.place(x = 950, y = 10, height=50, width=50)

root = tk.Tk()
root.title("Strap Vision System")

# root.geometry("1024x600")
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
canvas.pack()

img_a = Image.open("IMG/Strap_A.png")
img_a = img_a.resize((200, 200), Image.LANCZOS)
img_b = Image.open("IMG/Strap_B.png")
img_b = img_b.resize((200, 200), Image.LANCZOS)
img_c = Image.open("IMG/Strap_C.png")
img_c = img_c.resize((200, 200), Image.LANCZOS)
back = Image.open("IMG/Back.png")
back = back.resize((50, 50), Image.LANCZOS)




Turn_off = Image.open("IMG/Turn_off.png")
Turn_off = Turn_off.resize((75, 75), Image.LANCZOS)

img_a = ImageTk.PhotoImage(img_a)
img_b = ImageTk.PhotoImage(img_b)
img_c = ImageTk.PhotoImage(img_c)
back = ImageTk.PhotoImage(back)
Turn_off = ImageTk.PhotoImage(Turn_off)

index()

#Formula (1024 - (3 * 200)) / 4

label = tk.Label(canvas, text="", font=("Helvetica", 16))

root.mainloop()
