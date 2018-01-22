import cv2
import numpy as np
import hog
import time
import imProc
import SVM

# 0 calibration 1 detectin
appStatus = 0

#################TRAINING

hog_descriptors = hog.getHOG()
responses = hog.getResp()

print('Training SVM model ...')
model = SVM.SVM()
model.train(hog_descriptors, responses)



###################################### CAMERA CAPTURE
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print ("VideoCapture failed")
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,800)
iP = imProc.ImProc()
print('Camera Capturing  ... ')
while(True):
    ret, frame = cap.read()
    if ret == False:
        print("Frame is empty")

    #print("height and width : ", frame.shape)
    mask1 = cv2.resize(frame, (600, 800), interpolation=cv2.INTER_AREA)
    mask2 = mask1[0:800, 0:480]
    mask2 = cv2.GaussianBlur(mask2, (5, 5), 0)
    mHSV = cv2.cvtColor(mask2, cv2.COLOR_BGR2HSV)
    mask3 = iP.backgroungRemove(mask2, appStatus)
    if appStatus == 0:
        mask2 = iP.drawCalibrationPoints(mask2)
    #mask2 = iP.drawContours(mask2, mask3)

    # Display the resulting frame
    cv2.imshow('frame', mask2)
    cv2.imshow('frame1', mask3)
    cv2.imshow('frame2', mHSV)
    #mask2
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()