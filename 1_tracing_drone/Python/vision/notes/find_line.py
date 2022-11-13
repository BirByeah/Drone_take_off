import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
kernel = np.ones((9,9),np.uint8)
length = 500
while(1):
    _, frame = cap.read()
    frame_cpy = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_cpy = cv.morphologyEx(frame_cpy, cv.MORPH_OPEN, kernel)
    ret,edges=cv.threshold(frame_cpy,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    edges = cv.Laplacian(edges, cv.CV_8U)
    cv.imshow("edges", edges)
    lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=60, maxLineGap=25)
    try:
        for line in lines:
            (x1, y1, x2, y2) = line[0]
            cv.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
    except TypeError as e:
        pass
    cv.imshow("lines", frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()