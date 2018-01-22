import cv2
import numpy as np


class ImProc:
    # wybranie 7 pkt które znajdją sie na ręce
    #           a
    #       f       g
    #      b    c    d
    #       m       n
    #           e
    def __init__(self):
        self.aX = 240
        self.aY = 150
        self.bX = 170
        self.bY = 500
        self.cX = 240
        self.cY = 500
        self.dX = 310
        self.dY = 500
        self.eX = 240
        self.eY = 700
        self.fX = 200
        self.fY = 300
        self.gX = 280
        self.gY = 300
        self.mX = 200
        self.mY = 600
        self.nX = 280
        self.nY = 600

        self.avUpperT = np.array([0, 0, 0])
        self.avUpperTmn = np.array([0, 0, 0])
        self.avLowerT = np.array([0, 0, 0])
        self.avLowerTmn = np.array([0, 0, 0])
        self.kernel = np.ones((10, 10), np.uint8)
        self.pointColor = [255, 0, 0]


    def backgroungRemove(self, maskn, status):
        global a, b, c, d, f, g, e, m, n
        mHSV = cv2.cvtColor(maskn, cv2.COLOR_BGR2HSV)
        mHSV = cv2.medianBlur(mHSV, 5)
        cv2.blur(mHSV, (5, 5))
        cv2.dilate(mHSV, self.kernel, 1)
        cv2.erode(mHSV, self.kernel, 3)
        #cv2.split(mHSV)
        a = mHSV[self.aY, self.aX]
        b = mHSV[self.bY, self.bX]
        c = mHSV[self.cY, self.cX]
        d = mHSV[self.dY, self.dX]
        e = mHSV[self.eY, self.eX]
        f = mHSV[self.fY, self.fX]
        g = mHSV[self.gY, self.gX]
        m = mHSV[self.mY, self.mX]
        n = mHSV[self.nY, self.nX]
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
        mTresh2 = cv2.inRange(mHSV, self.avLowerTmn, self.avUpperTmn)
        maskedImg = cv2.bitwise_and(mTresh, mTresh2)
        print("avLowerT = ", self.avLowerT)
        print("avUpperT = ", self.avUpperT)
        cv2.blur(maskedImg, (5,5))
        cv2.dilate(maskedImg, self.kernel, 1)
        cv2.erode(maskedImg, self.kernel, 3)
        return maskedImg



    def drawContours( self, frame, maskn):
        im2, contours, hierarchy = cv2.findContours(maskn, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(maskn, contours, 3, (0, 255, 0), 3)
        #mRgba, contours, hierarhy = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return maskn

    def drawCalibrationPoints(self, maskn):
        cv2.rectangle(maskn, (self.aX - 5, self.aY - 5), (self.aX + 5, self.aY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.bX - 5, self.bY - 5), (self.bX + 5, self.bY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.cX - 5, self.cY - 5), (self.cX + 5, self.cY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.dX - 5, self.dY - 5), (self.dX + 5, self.dY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.eX - 5, self.eY - 5), (self.eX + 5, self.eY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.fX - 5, self.fY - 5), (self.fX + 5, self.fY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.gX - 5, self.gY - 5), (self.gX + 5, self.gY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.mX - 5, self.mY - 5), (self.mX + 5, self.mY + 5), (0, 255, 0))
        cv2.rectangle(maskn, (self.nX - 5, self.nY - 5), (self.nX + 5, self.nY + 5), (0, 255, 0))
        maskn[self.aY, self.aX] = self.pointColor
        maskn[self.bY, self.bX] = self.pointColor
        maskn[self.cY, self.cX] = self.pointColor
        maskn[self.dY, self.dX] = self.pointColor
        maskn[self.eY, self.eX] = self.pointColor
        maskn[self.fY, self.fX] = self.pointColor
        maskn[self.gY, self.gX] = self.pointColor
        maskn[self.mY, self.mX] = self.pointColor
        maskn[self.nY, self.nX] = self.pointColor
        return maskn

    def calibrationOfTreshold(self):
        values = []
        valuesmn = []
        # avLowerT = np.array([0, 0, 0])
        # avUpperT = np.array([0, 0, 0])
        upper = [0, 0, 0]
        lower = [0, 0, 0]
        uppermn = [0, 0, 0]
        lowermn = [0, 0, 0]
        for i in range(0,3):
            values.append(a[i])
            values.append(b[i])
            values.append(c[i])
            values.append(d[i])
            values.append(f[i])
            values.append(g[i])
            sorted(values)
            valuesmn.append(e[i])
            valuesmn.append(m[i])
            valuesmn.append(n[i])
            sorted(valuesmn)
            lower[i] = values[0]
            upper[i] = values[5] #6
            lowermn[i] = valuesmn[0]
            uppermn[i] = valuesmn[2] #6
            #print("A = %d\n" % a[i])
            # print(" B = %d\n" % b[i])
            # print(" C = %d\n" % c[i])
            # print(" D = %d\n" % d[i])
            # print(" E = %d\n" % e[i])
            # print(" F = %d\n" % f[i])
            # print(" G = %d\n" % g[i])
            values.clear()
            valuesmn.clear()
        #self.avUpperT = np.asarray([upper[0] + 20, upper[1] + 20, 255])
        self.avUpperT = np.asarray([upper[0] + 10, upper[1] + 5, 255])
        self.avUpperTmn = np.asarray([uppermn[0] + 10, uppermn[1] + 5, 255])
        #self.avUpperT = np.asarray([upper[0], upper[1], upper[2]])
        self.avLowerT = np.asarray([lower[0] -10, lower[1] - 2, 0])
        self.avLowerTmn = np.asarray([lowermn[0] -10, lowermn[1] - 2, 0])
        #self.avLowerT = np.asarray([lower[0], lower[1], lower[2]])
        #print("Upper value for H=%d    S=%d    V=%d" %avUpperT.val[0] %avUpperT.val[1] %avUpperT.val[2])
        #print("Lower value for H=%d    S=%d    V=%d" %avLowerT.val[0] %avLowerT.val[1] %avLowerT.val[2])