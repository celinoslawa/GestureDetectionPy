import cv2
import numpy as np
import hog
import time
import imProc
from enum import Enum

class StatModel(object):
    def load(self, fn):
        self.model.load(fn)  # Known bug: https://github.com/opencv/opencv/issues/4969
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    def __init__(self, C = 12.5, gamma = 0.50625):
        self.model = cv2.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv2.ml.SVM_RBF)
        #self.model.setKernel(cv2.ml.SVM_LINEAR)
        self.model.setType(cv2.ml.SVM_C_SVC)

    def train(self, samples, responses):
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    def predict(self, samples):

        return self.model.predict(samples)[1].ravel()

    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1
        print('Goodbye!\n\n\n\n\n')



# 0 calibration 1 detectin
appStatus = 0

#################TRAINING

hog_descriptors = hog.getHOG()
responses = hog.getResp()

print('Training SVM model ...')
model = SVM()
model.train(hog_descriptors, responses)



###################################### CAMERA CAPTURE
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print ("VideoCapture failed")
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,800)

while(True):
    ret, frame = cap.read()
    if ret == False:
        print("Frame is empty")

    #print("height and width : ", frame.shape)
    mask1 = cv2.resize(frame, (600, 800), interpolation=cv2.INTER_AREA)
    mask2 = mask1[0:800, 0:480]
    mHSV = cv2.cvtColor(mask2, cv2.COLOR_BGR2HSV)
    mask3 = imProc.backgroungRemove(mask2, appStatus)
    if appStatus == 0:
        mask2 = imProc.drawCalibrationPoints(mask2)
    mask2 = imProc.drawContours(mask2,mask3)

    # Display the resulting frame
    cv2.imshow('frame', mask2)
    #mask2
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()