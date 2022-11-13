import cv2 as cv
import numpy as np

img = np.zeros((201, 201, 3))
img = cv.circle(img, (100, 100), 50, (255, 255, 255), -1)
cv.imshow("img", img)
cv.imwrite("img.jpg", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.destroyAllWindows()
