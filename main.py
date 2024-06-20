import cv2
import mediapipe as mp   

cap = cv2.VideoCapture(0)
mediapipehands = mp.solutions.hands  
hands = mediapipehands.Hands()

Draw = mp.solutions.drawing_utils

while True:
    _ , frame = cap.read()
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(frameRGB)
    
    if result.multi_hand_landmarks:
        for handlandmarks in result.multi_hand_landmarks:
            for id , landmark in enumerate(handlandmarks.landmark):
                h,w,c = frame.shape
                x , y = int(landmark.x*w),int(landmark.y*h)
                print(id,x,y)
                if id == 8 or id == 4:
                    cv2.circle(frame,(x,y),10,(0,0,255),3)
            Draw.draw_landmarks(frame,handlandmarks,mediapipehands.HAND_CONNECTIONS)
            
    cv2.imshow('webcam',frame)
    if cv2.waitKey(1) & 0xFF == 113:
        break