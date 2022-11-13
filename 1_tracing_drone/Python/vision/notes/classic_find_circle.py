import numpy as np
import cv2 as cv


#cap = cv.VideoCapture(0)
img = cv.imread("img.jpg")
#ret, img = cap.read()
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.GaussianBlur(img, (7, 7), 1.5, sigmaY=1.5)
circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                            param1=50,param2=50,maxRadius=-1)
try:
    circles = np.uint16(np.around(circles))
except Exception:
    pass
print(circles)
for i in circles[0,:]:
    # draw the center of the circle
    cv.circle(img,(i[0],i[1]),2,(0,255,0),3)

cv.imshow('detected circles',img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.destroyAllWindows()

"""import numpy as np
import cv2 as cv


#cap = cv.VideoCapture(0)
img = cv.imread("img.jpg")
while True:
    #ret, img = cap.read()
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (7, 7), 1.5, sigmaY=1.5)
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=60,param2=60,maxRadius=-1)
    try:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the center of the circle
            cv.circle(img,(i[0],i[1]),2,(0,0,0),3)
    except Exception:
        pass
    cv.imshow('detected circles',img)
    if cv.waitKey(1) & 0xFF == ord('q'):
       break
cv.waitKey(0)
cv.destroyAllWindows()"""