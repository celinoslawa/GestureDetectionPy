import cv2
import numpy as np

global a
global b
global c
global d
global e
global f
global g
# a = [0, 0, 0]
# b = [0, 0, 0]
# c = [0, 0, 0]
# d = [0, 0, 0]
# e = [0, 0, 0]
# f = [0, 0, 0]
# g = [0, 0, 0]

    # wybranie 7 pkt które znajdją sie na ręce

    #           a
    #       f       g
    #      b    c    d
    #
    #           e
aX = 240
aY = 200
bX = 170
bY = 400
cX = 240
cY = 400
dX = 310
dY = 400
eX = 240
eY = 600
fX = 180
fY = 300
gX = 300
gY = 300
#avUpperT = np.array([0, 0, 0])
#avLowerT = np.array([0, 0, 0])
kernel = np.ones((5, 5), np.uint8)
pointColor = [255, 0, 0]


def backgroungRemove(frame, status):
    mHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.split(mHSV)
    a = mHSV[aY, aX]
    b = mHSV[bY, bX]
    c = mHSV[cY, cX]
    d = mHSV[dY, dX]
    e = mHSV[eY, eX]
    f = mHSV[fY, fX]
    g = mHSV[gY, gX]
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)
    # print(g)
    #mTresh = frame
    if (status == 0):
        calibrationOfTreshold(a, b, c, d, e, f, g)
    mTresh = cv2.inRange(mHSV, avLowerT, avUpperT)
    print("avLowerT = ", avLowerT)
    print("avUpperT = ", avUpperT)
    #cv2.convert
    #mTresh.convertTo(mTresh,cv2.CV_8UC1)
    cv2.blur(mTresh, (5, 5))
    cv2.dilate(mTresh, kernel, 1)
    cv2.erode(mTresh, kernel, 3)
    return mTresh



def drawContours( mRgba, mask):
    #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mRgba, contours, hierarhy = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.findContours(mask, contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(0,len(contours)):
        if(cv2.contourArea(contours[i])>= 7000):
            scontours = []
            scontours.append(contours[i])
            cv2.drawContours(mRgba,scontours,-1, (255,0,0),5)
    return mRgba

def drawCalibrationPoints(frame):
    cv2.rectangle(frame, (aX - 5, aY - 5), (aX + 5, aY + 5), (0, 0, 0))
    cv2.rectangle(frame, (bX - 5, bY - 5), (bX + 5, bY + 5), (0, 0, 0))
    cv2.rectangle(frame, (cX - 5, cY - 5), (cX + 5, cY + 5), (0, 0, 0))
    cv2.rectangle(frame, (dX - 5, dY - 5), (dX + 5, dY + 5), (0, 0, 0))
    cv2.rectangle(frame, (eX - 5, eY - 5), (eX + 5, eY + 5), (0, 0, 0))
    cv2.rectangle(frame, (fY - 5, fY - 5), (fX + 5, fY + 5), (0, 0, 0))
    cv2.rectangle(frame, (gX - 5, gY - 5), (gX + 5, gY + 5), (0, 0, 0))
    frame[aY, aX] = pointColor
    frame[bY, bX] = pointColor
    frame[cY, cX] = pointColor
    frame[dY, dX] = pointColor
    frame[eY, eX] = pointColor
    frame[fY, fX] = pointColor
    frame[gY, gX] = pointColor
    return frame

def calibrationOfTreshold(a, b, c, d, e, f, g):
    values = []
    global avLowerT
    global avUpperT
    avLowerT = np.array([0, 0, 0])
    avUpperT = np.array([0, 0, 0])
    upper = [0, 0, 0]
    lower = [0, 0, 0]
    for i in range(0,3):
        values.append(a[i])
        values.append(b[i])
        values.append(c[i])
        values.append(d[i])
        values.append(e[i])
        values.append(f[i])
        values.append(g[i])
        sorted(values)
        lower[i] = values[0]
        upper[i] = values[6]
        #print("A = %d\n" % a[i])
        # print(" B = %d\n" % b[i])
        # print(" C = %d\n" % c[i])
        # print(" D = %d\n" % d[i])
        # print(" E = %d\n" % e[i])
        # print(" F = %d\n" % f[i])
        # print(" G = %d\n" % g[i])
        values.clear()
        avUpperT = [upper[0] + 20, upper[1] + 20, 255]
        avLowerT = [lower[0], lower[1], 0]
        #print("Upper value for H=%d    S=%d    V=%d" %avUpperT.val[0] %avUpperT.val[1] %avUpperT.val[2])
        #print("Lower value for H=%d    S=%d    V=%d" %avLowerT.val[0] %avLowerT.val[1] %avLowerT.val[2])