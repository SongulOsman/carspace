import cv2
import pickle 

width, height = 27, 15

try:
    with open("ArabaParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    
    if events == cv2.EVENT_LBUTTONDOWN: # sol click
        posList.append((x, y)) # x ve y koordinatlarında gösterir
    
    if events == cv2.EVENT_RBUTTONDOWN: # sağ click ile seçilen dikdörtgenleri siler
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height: # işaretli dikdörtgenlerin içindeyse listeden siler
                posList.pop(i)
        with open("ArabaParkPos","wb") as f: 
            pickle.dump(posList, f)

while True:
    
    img = cv2.imread("OtoparkAlanResim.png" )
    
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (236,110,179),2) # pozisyon list içinde bulunan her x , y için dikdörtgen çizer
    # print("poslist: ",posList)
    
    cv2.imshow("img",img)
    cv2.setMouseCallback("img", mouseClick)
    cv2.waitKey(1)
