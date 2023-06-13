import cv2
import pickle
import numpy as np

def checkParkSpace(resim):
    spaceCounter = 0 # boşlukları tutan değişken
    
    for pos in posList:
        x, y = pos
        
        img_crop = resim[y: y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        
        # print("count: ", count) # her dikdörtgen içerisindeki pikselleri sayar
        
        if count < 150: # işaretli olan boş ise çalışır
            color = (127, 255, 0)
            spaceCounter += 1
        else: # doluysa çalışır
            color = (255,0, 0,)
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2) 
        cv2.putText(img, str(count), (x, y + height - 2),cv2.FONT_HERSHEY_PLAIN, 1,color,1)
    
    cv2.putText(img, f"BosAlan: {spaceCounter}/{len(posList)}", (7,22), cv2.FONT_HERSHEY_PLAIN, 2,(78,27,255),2)


width = 27
height = 15


cap = cv2.VideoCapture("OtoparkAlanVideo.mp4")

with open("ArabaParkPos", "rb") as f:
    posList = pickle.load(f)

while True:
    success, img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)
    
    checkParkSpace(imgDilate)
    cv2.imshow("img", img)
    #cv2.imshow("img_gray", imgGray)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThreshold", imgThreshold)
    # cv2.imshow("imgMedian", imgMedian)
    # cv2.imshow("imgDilate", imgDilate)
    cv2.waitKey(150)
