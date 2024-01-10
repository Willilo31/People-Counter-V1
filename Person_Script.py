import cv2
from ultralytics import YOLO

def main():
    model = YOLO("yolov8s.pt")
    class_names = ["Person"]
    
    cap = cv2.VideoCapture(0)
    
    Start_Line = 300
    # End_Line = 400

    counter = 0
    id_matrix = []

    while True:
        ret, frame = cap.read()        
        
        if not ret:
            continue

        height, width, _ = frame.shape

        results = model.track(frame, verbose=False, agnostic_nms=True, persist=True)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()

            for box, id, class_id, confidence in zip(boxes, ids, class_ids, confidences):
                x1, y1, x2, y2 = box
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                if class_id == 0:  #Bottle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                    cv2.putText(frame, f"ID #{id} {class_names[0]} {confidence:.2f}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                    id_exists = False
                    for row in id_matrix:
                        if row[0] == id:
                            id_exists = True
                            
                            if center_x >= Start_Line and not row[1]: #  |. -> .|
                                row[1] = True
                                counter += 1  

                            if center_x <= Start_Line and row[1]:  # .|  ->  |.
                                row[1] = False
                                counter -= 1                  
                        
                    if not id_exists:
                        if center_x <= Start_Line:
                            # counter += 1
                            print("Persona Entrando")
                            id_matrix.append([id, False])

                        if center_x >= Start_Line:
                            # counter -= 1
                            print("Persona Saliendo")
                            id_matrix.append([id, True])
                        
                    #     # Marcar el ID como "Salida" en la matriz
                    #     for row in id_matrix:
                    #         if row[0] == id:
                    #             row[2] = True

                    # if center_x <= Start_Line:
                    #     print("Entrada")

                    # if center_x >= End_Line:
                    #     print("Salida")

                    center_x = 0
                    center_y = 0


        cv2.putText(frame, f"Contador {counter}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,)
        cv2.putText(frame, f"Entrada", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
        cv2.putText(frame, f"Salida", (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
        cv2.line(frame, (Start_Line, 0), (Start_Line, height), (255, 255, 255), 3)
        # cv2.line(frame, (End_Line, 0), (End_Line, height), (0, 0, 0), 3)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()