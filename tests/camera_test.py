import cv2 as cv
import threading

cap = cv.VideoCapture(0)
def open_camera():
    while True:
        ret, img = cap.read()
        if ret == False:
            print("Camera can't be opened.")
            continue
        cv.imshow("photo", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

thread_open_camera = threading.Thread(None, open_camera, "camera")
thread_open_camera.start()
