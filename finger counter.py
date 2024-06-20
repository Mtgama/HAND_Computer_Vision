import cv2
import mediapipe as mp
import madule_test as hm

green = (0,255,0)

cap = cv2.VideoCapture(0)
detector = hm.HandDetector(detectionCon = 0.6)
Indexes = [4,8,12,16,20]
while True:
    _, frame = cap.read()
    frame = detector.findHand(frame)
    landmarkList = detector.handPosition(frame, draw=True,handno=0)
    
    if len(landmarkList) != 0:
        fingers = []
        #if landmarkList[8][2] < landmarkList[6][2]:
            #print('Open')
        # 4 fingers
        for index in range(1,5):
            if landmarkList[Indexes[index]][2] < landmarkList[Indexes[index] - 2][2]:
                print(landmarkList[Indexes[index]][2],landmarkList[Indexes[index] - 2][2])
                fingers.append(1)
            else:
                fingers.append(0)

        # Thumb
        if landmarkList[Indexes[0]][1] > landmarkList[Indexes[0] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        number_of_fingers = fingers.count(1)
        print(number_of_fingers)
        cv2.putText(frame , f"number of finger:{str(number_of_fingers)}" , (50,100) , cv2.FONT_HERSHEY_PLAIN
                    , 3, green , 4)
        #print(fingers)
    cv2.imshow('Finger Counter', frame)
    if cv2.waitKey(1) & 0xFF == 113:
        break