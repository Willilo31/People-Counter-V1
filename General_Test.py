import cv2
from ultralytics import YOLO
import time

model = YOLO('Heads_IT.pt')
url = 'http://root:admin@192.168.0.11/axis-cgi/mjpg/video.cgi'
cap = cv2.VideoCapture(url)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Inicializar el tiempo
prev_frame_time = time.time()
new_frame_time = 0

while cap.isOpened():
    success, frame = cap.read()

    if success:
        new_frame_time = time.time()

        results = model(frame, device=0, imgsz=640, conf=0.50, agnostic_nms=True)
        annotated_frame = results[0].plot()

        # Calcula FPS
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        
        # Convierte el FPS a string para mostrarlo
        fps_text = f"FPS: {fps:.2f}"

        # Pone el FPS en el frame
        cv2.putText(annotated_frame, fps_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Frame", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
