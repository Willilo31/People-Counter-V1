import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import imutils
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import subprocess

def visualizar():
    global inicio, cap, frame, model, class_names, counter, personas, id_matrix, Start_Line, max_cap, hora_actual
    global texto1, texto2, texto3, texto4, time_now, warning_msg, bg_id, BoxShadow_id
    
    if inicio == 1:
        model = YOLO("yolov8s.pt")
        cap = cv2.VideoCapture(0)
        cap.set(4, 640)
        cap.set(3, 480)
        class_names = ["Person"]
        inicio = 0
        counter = 6
        personas = 14
        id_matrix = []
        Start_Line = 320
        max_cap = 10
        warning_msg = False
        texto1 = pantalla.create_text(550, 113, text="People Counter Vision System", font=("Helvetica", 35, "bold"), fill="white")
    else:
        pantalla.delete(frame)
        pantalla.delete(texto2)
        pantalla.delete(texto3)
        pantalla.delete(texto4)
        pantalla.delete(time_now)
        pantalla.delete(bg_id)
        # pantalla.delete(Corner_id)
        pantalla.delete(BoxShadow_id)

    hora_actual = datetime.now().strftime("%H:%M:%S")
    if counter < 8:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgBlue)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        # Corner_id = pantalla.create_image(309, 400, anchor=tk.NW, image=Corner_Yellow)
        texto2 = pantalla.create_text(1315, 400, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="white")
        texto3 = pantalla.create_text(1323, 550, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="white")
        texto4 = pantalla.create_text(1337, 700, text=f"Today's Entries: {personas:03} ", font=("Helvetica", 35, "bold"), fill="white")
        time_now = pantalla.create_text(625, 820, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="white")
        warning_msg = False
    elif counter < 10:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgYellow)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        # Corner_id = pantalla.create_image(309, 300, anchor=tk.NW, image=Corner_Yellow)
        texto2 = pantalla.create_text(1315, 400, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="black")
        texto3 = pantalla.create_text(1323, 550, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="black")
        texto4 = pantalla.create_text(1337, 700, text=f"Today's Entries: {personas:03} ", font=("Helvetica", 35, "bold"), fill="black")
        time_now = pantalla.create_text(625, 820, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="black")
        if warning_msg == False:
            warning_msg = True
            subprocess.Popen(["python3", "mensaje2.py"])
    else:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgRed)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        # Corner_id = pantalla.create_image(309, 300, anchor=tk.NW, image=Corner_Red)
        texto2 = pantalla.create_text(1315, 400, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="white")
        texto3 = pantalla.create_text(1323, 550, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="white")
        texto4 = pantalla.create_text(1337, 700, text=f"Today's Entries: {personas:03} ", font=("Helvetica", 35, "bold"), fill="white")
        time_now = pantalla.create_text(625, 820, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="white")

    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.track(frame, verbose=True, agnostic_nms=True, persist=True, conf = 0.10)
            height, width, _ = frame.shape

            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                confidences = results[0].boxes.conf.cpu().numpy()

                for box, id, class_id, confidence in zip(boxes, ids, class_ids, confidences):
                    x1, y1, x2, y2 = box
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    if class_id == 0: 
                        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                        # cv2.putText(frame, f"ID #{id} {class_names[0]} {confidence:.2f}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                        # cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)

                        id_exists = False
                        for row in id_matrix:
                            if row[0] == id:
                                id_exists = True
                                
                                if center_x >= Start_Line and not row[1]: #  |. -> .|
                                    row[1] = True
                                    counter += 1
                                    personas += 1   

                                if center_x <= Start_Line and row[1]:  # .|  ->  |.
                                    row[1] = False
                                    counter -= 1                  
                            
                        if not id_exists:
                            if center_x <= Start_Line:
                                # print("Persona Entrando")
                                id_matrix.append([id, False])

                            if center_x >= Start_Line:
                                # print("Persona Saliendo")
                                id_matrix.append([id, True])
                        center_x = 0
                        center_y = 0

            # cv2.line(frame, (Start_Line, 0), (Start_Line, height), (255, 255, 255), 3)
            # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            pantalla.after(10, visualizar)
        else:
            cap.release()


def turn_off_action():
    root.destroy()

root = tk.Tk()
root.title("People Counter Vision System")

#root.geometry("1920x1080")
root.attributes('-fullscreen', True)

pantalla = tk.Canvas(root, width=1920, height=1080, bg="#0E131F")
pantalla.pack()

#Logo de Baxter
Logo = tk.PhotoImage(file="IMG/logoBaxter.png")
Baxter_Logo = pantalla.create_image(1693, 945, anchor=tk.NW, image=Logo)

#Backgrounds
bgBlue = tk.PhotoImage(file="IMG/bgBlue.png")
bgRed= tk.PhotoImage(file="IMG/bgRed.png")
bgYellow= tk.PhotoImage(file="IMG/bgYellow.png")

#Corners
Corner_Blue= tk.PhotoImage(file="IMG/CornerBlue.png")
Corner_Red= tk.PhotoImage(file="IMG/CornerRed.png")
Corner_Yellow = tk.PhotoImage(file="IMG/CornerYellow.png")
BoxShadow = tk.PhotoImage(file="IMG/BoxShadow.png")

#Imagen Demo
# demo = tk.PhotoImage(file="IMG/imageDemo.png")


#Boton de cerrado
Close = tk.PhotoImage(file="IMG/x-circle.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#0E131F", command=turn_off_action)
Close_Button.place(x = 1794, y = 55)

lblVideo = tk.Label(pantalla)
lblVideo.configure(borderwidth=0)
# lblVideo.configure(padx=0, pady=0)
lblVideo.place(x = 309, y = 300)
inicio = 1

visualizar()

root.mainloop()
