import cv2
import numpy as np


def empty(x):
    pass


points = []


def getContours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y = 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x, y


colors = [[0, 120, 184, 179, 255, 255],
          [104, 80, 160, 179, 255, 255]]


colorV = [[0, 255, 255], [255, 0, 0]]


def detectColor(image, color):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    P = []
    for clr in color:
        lower = np.array(clr[0:3])
        upper = np.array(clr[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            P.append([x, y, color.index(clr)])
    return P


frameWidth = 640
frameHeight = 480
cap = cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 200)


def Draw(points):
    for point in points:
        cv2.circle(Result, (point[0], point[1]), 10, colorV[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    Result = img.copy()
    P = detectColor(img, colors)
    if len(P) != 0:
        for point in P:
            points.append(point)
    if len(points) != 0:
        Draw(points)
    cv2.imshow("Result", Result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
