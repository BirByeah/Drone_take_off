import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
kernel = np.ones((9,9),np.uint8)
circle_img = np.zeros((201, 201, 1))
cv.circle(circle_img, (100, 100), 50, (255), -1)
contours_, hierarchy_ = cv.findContours(circle_img, 2, 1)
sim_list = []

while True:
    _, frame = cap.read()
    list.clear()
    frame_cpy = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_cpy = cv.morphologyEx(frame_cpy, cv.MORPH_OPEN, kernel)
    ret, binary=cv.threshold(frame_cpy,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for i in range(hierarchy.shape[0]):
        sim_list.append(cv.matchShapes(contours_,contours[i],1,0.0))
    index = np.argmin(np.array(sim_list))
    cv.drawContours(frame, contours, index, (0, 0, 255), 2)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()