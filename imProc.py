import cv2
import numpy as np


class ImProc:
    #global a
    #global b
    #global c
    #global d
    #global e
    #global f
    #global g
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
    def __init__(self):
        self.aX = 240
        self.aY = 200
        self.bX = 170
        self.bY = 400
        self.cX = 240
        self.cY = 400
        self.dX = 310
        self.dY = 400
        self.eX = 240
        self.eY = 600
        self.fX = 180
        self.fY = 300
        self.gX = 300
        self.gY = 300
        self.avUpperT = np.array([0, 0, 0])
        self.avLowerT = np.array([0, 0, 0])
        self.kernel = np.ones((5, 5), np.uint8)
        self.pointColor = [255, 0, 0]


    def backgroungRemove(self, frame, status):
        global a, b, c, d, e, f, g
        mHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.split(mHSV)
        a = mHSV[self.aY, self.aX]
        b = mHSV[self.bY, self.bX]
        c = mHSV[self.cY, self.cX]
        d = mHSV[self.dY, self.dX]
        e = mHSV[self.eY, self.eX]
        f = mHSV[self.fY, self.fX]
        g = mHSV[self.gY, self.gX]
        # print(a)
        # print(b)
        # print(c)
        # print(d)
        # print(e)
        # print(f)
        # print(g)
        #mTresh = frame
        if (status == 0):
            self.calibrationOfTreshold()
        mTresh = cv2.inRange(mHSV, self.avLowerT, self.avUpperT)
        print("avLowerT = ", self.avLowerT)
        print("avUpperT = ", self.avUpperT)
        #cv2.convert
        #mTresh.convertTo(mTresh,cv2.CV_8UC1)
        cv2.blur(mTresh, (5, 5))
        cv2.dilate(mTresh, self.kernel, 1)
        cv2.erode(mTresh, self.kernel, 3)
        return mTresh



    def drawContours( self, mRgba, mask):
        #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mRgba, contours, hierarhy = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #cv2.findContours(mask, contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(0,len(contours)):
            if(cv2.contourArea(contours[i])>= 7000):
                scontours = []
                scontours.append(contours[i])
                cv2.drawContours(mRgba,scontours,-1, (255,0,0),5)
        return mRgba

    def drawCalibrationPoints(self, frame):
        cv2.rectangle(frame, (self.aX - 5, self.aY - 5), (self.aX + 5, self.aY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.bX - 5, self.bY - 5), (self.bX + 5, self.bY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.cX - 5, self.cY - 5), (self.cX + 5, self.cY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.dX - 5, self.dY - 5), (self.dX + 5, self.dY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.eX - 5, self.eY - 5), (self.eX + 5, self.eY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.fY - 5, self.fY - 5), (self.fX + 5, self.fY + 5), (0, 0, 0))
        cv2.rectangle(frame, (self.gX - 5, self.gY - 5), (self.gX + 5, self.gY + 5), (0, 0, 0))
        frame[self.aY, self.aX] = self.pointColor
        frame[self.bY, self.bX] = self.pointColor
        frame[self.cY, self.cX] = self.pointColor
        frame[self.dY, self.dX] = self.pointColor
        frame[self.eY, self.eX] = self.pointColor
        frame[self.fY, self.fX] = self.pointColor
        frame[self.gY, self.gX] = self.pointColor
        return frame

    def calibrationOfTreshold(self):
        values = []
        # avLowerT = np.array([0, 0, 0])
        # avUpperT = np.array([0, 0, 0])
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
        self.avUpperT = np.asarray([upper[0] + 20, upper[1] + 20, 255])
        self.avLowerT = np.asarray([lower[0], lower[1], 0])
        #print("Upper value for H=%d    S=%d    V=%d" %avUpperT.val[0] %avUpperT.val[1] %avUpperT.val[2])
        #print("Lower value for H=%d    S=%d    V=%d" %avLowerT.val[0] %avLowerT.val[1] %avLowerT.val[2])