import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import paramiko

def leer_valor_personas():
    try:
        with open("Personas", "r") as file:
            return int(file.read())
    except:
        return 0

def guardar_valor_personas(valor):
    with open("Personas", "w") as file:
        file.write(str(valor))

def visualizar():
    global inicio, cap, frame, model, class_names, counter, id_matrix, Start_Line, max_cap, hora_actual
    global texto1, texto2, texto3, time_now, bg_id, BoxShadow_id, text_desarrollo
   
    if inicio == 1:
        url = 'http://root:jetson@192.168.0.12/axis-cgi/mjpg/video.cgi' #'http://root:jetson@10.62.80.139/axis-cgi/mjpg/video.cgi'
        model = YOLO("Heads_IT.pt")
        cap = cv2.VideoCapture(url)
        cap.set(4, 640)
        cap.set(3, 480)
        class_names = model.names
        inicio = 0
        counter = leer_valor_personas()
        id_matrix = []
        Start_Line = 200
        max_cap = 1334
        texto1 = pantalla.create_text(210, 90, text="People Counter Vision System - Beta", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
        text_desarrollo = pantalla.create_text(221, 965, text="Software Under Development", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)
    else:
        pantalla.delete(frame)
        pantalla.delete(texto2)
        pantalla.delete(texto3)
        pantalla.delete(time_now)
        pantalla.delete(bg_id)
        # pantalla.delete(Corner_id)
        pantalla.delete(BoxShadow_id)
        counter = leer_valor_personas()

    hora_actual = datetime.now().strftime("%H:%M:%S")
    if counter < max_cap*0.8:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgBlue)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        texto2 = pantalla.create_text(1103, 388, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
        texto3 = pantalla.create_text(1103, 609, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
        time_now = pantalla.create_text(500, 800, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

    elif counter < max_cap:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgYellow)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        texto2 = pantalla.create_text(1103, 388, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="black", anchor=tk.NW)
        texto3 = pantalla.create_text(1103, 609, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="black", anchor=tk.NW)
        time_now = pantalla.create_text(500, 800, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)

    else:
        bg_id = pantalla.create_image(210, 167, anchor=tk.NW, image=bgRed)
        BoxShadow_id = pantalla.create_image(284, 275, anchor=tk.NW, image=BoxShadow)
        # Corner_id = pantalla.create_image(309, 300, anchor=tk.NW, image=Corner_Red)
        texto2 = pantalla.create_text(1103, 388, text=f"People Inside: {counter:02}    ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
        texto3 = pantalla.create_text(1103, 609, text=f"Max Capacity: {max_cap:02}     ", font=("Helvetica", 35, "bold"), fill="white", anchor=tk.NW)
        time_now = pantalla.create_text(500, 800, text=f"Time: {hora_actual}", font=("Helvetica", 30, "bold"), fill="white", anchor=tk.NW)


    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.track(frame, verbose=True, agnostic_nms=True, persist=True, conf = 0.30)
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
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                        cv2.putText(frame, f"ID #{id} {class_names[class_id]} {confidence:.2f} {len(id_matrix)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)

                        id_exists = False
                        for row in id_matrix:
                            if row[0] == id:
                                id_exists = True

                                if center_y >= Start_Line and not row[1]: #  |. -> .|
                                    row[1] = True
                                    counter -= 1
                                    guardar_valor_personas(counter)  
                                if center_y <= Start_Line and row[1]:  # .|  ->  |.
                                    row[1] = False
                                    counter += 1
                                    guardar_valor_personas(counter)  
                        if not id_exists:
                            if center_y <= Start_Line:
                                # print("Persona Entrando")
                                id_matrix.append([id, False])

                            if center_y >= Start_Line:
                                # print("Persona Saliendo")
                                id_matrix.append([id, True])
                        center_x = 0
                        center_y = 0
                        if len(id_matrix) >= 10:
                            for _ in range(5):
                                id_matrix.pop(0)

            # cv2.line(frame, (Start_Line, 0), (Start_Line, height), (255, 255, 255), 3)
            cv2.line(frame, (0, Start_Line), (width, Start_Line), (255, 255, 255), 3)
            # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            pantalla.after(1, visualizar)
        else:
            cap.release()
            url = 0 #'http://root:jetson@10.62.80.139/axis-cgi/mjpg/video.cgi'
            cap = cv2.VideoCapture(url)
            cap.set(4, 640)
            cap.set(3, 480)
            pantalla.after(10, visualizar)
    
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

#Boton de cerrado
Close = tk.PhotoImage(file="IMG/x-circle.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#0E131F", command=turn_off_action, borderwidth=0, relief="flat", highlightthickness=0)
Close_Button.place(x = 1794, y = 55)

lblVideo = tk.Label(pantalla)
lblVideo.configure(borderwidth=0)
# lblVideo.configure(padx=0, pady=0)
lblVideo.place(x = 309, y = 300)
inicio = 1

visualizar()

root.mainloop()