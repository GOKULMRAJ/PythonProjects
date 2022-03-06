import cv2
import numpy as np

frameWidth = 320
frameHeight = 320
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def empty(a):
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:

    success, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    minh = cv2.getTrackbarPos("HUE Min", "HSV")
    maxh = cv2.getTrackbarPos("HUE Max", "HSV")
    mins = cv2.getTrackbarPos("SAT Min", "HSV")
    maxs = cv2.getTrackbarPos("SAT Max", "HSV")
    minv = cv2.getTrackbarPos("VALUE Min", "HSV")
    maxv = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([minh, mins, minv])
    upper = np.array([maxh, maxs, maxv])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stack', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
