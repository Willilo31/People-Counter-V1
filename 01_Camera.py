import cv2

camera_url = 'http://root:jetson@192.168.0.12/axis-cgi/mjpg/video.cgi'
camera_url2 = 'http://root:admin@192.168.0.11/axis-cgi/mjpg/video.cgi'

cap = cv2.VideoCapture(camera_url)
cap2 = cv2.VideoCapture(camera_url2)

# Configura el tamaño de la ventana de visualización
cv2.namedWindow('Video Stream 1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video Stream 1', 800, 600)

cv2.namedWindow('Video Stream 2', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video Stream 2', 800, 600)

while True:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    # if not ret:
    #     print("Error al leer el frame.")
    #     break

    cv2.imshow('Video Stream 1', frame)
    cv2.imshow('Video Stream 2', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # time.sleep(0.1)

cap.release()
cap2.release()
cv2.destroyAllWindows()


