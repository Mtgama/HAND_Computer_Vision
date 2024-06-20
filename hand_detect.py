import numpy as np               
import mediapipe as mp         
import cv2

mphands = mp.solutions.hands
hands = mphands.Hands()
cap = cv2.VideoCapture(0)

Draw = mp.solutions.drawing_utils

while True:
    _ , frame = cap.read()
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(frameRGB)
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for handlandmarks in result.multi_hand_landmarks:
            for id , lndmark in enumerate(handlandmarks.landmark):
                h,w,c = frame.shape
                x , y = int(lndmark.x*w) , int(lndmark.y*h)
                print(id,x,y)
                
                if id == 4:
                    cv2.circle(frame,(x,y),15,(255,0,0),3)
                if id == 8:
                    cv2.circle(frame,(x,y),15,(0,255,0),3)
                Draw.draw_landmarks(frame,handlandmarks,mphands.HAND_CONNECTIONS)
    cv2.imshow('webcam',frame)
    if cv2.waitKey(1) & 0xFF ==27:
        break
    
