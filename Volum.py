import cv2
import numpy as np
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# تنظیمات MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# تنظیمات Pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

# تنظیمات دوربین
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # تبدیل تصویر به RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # شناسایی دست‌ها
        results = hands.process(image)
        
        # تبدیل تصویر به BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # گرفتن مختصات انگشت شست و اشاره
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                h, w, c = image.shape
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                
                # رسم دایره بر روی نوک انگشت شست و اشاره
                cv2.circle(image, (thumb_x, thumb_y), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(image, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)
                cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)
                
                # محاسبه فاصله بین نوک انگشت شست و اشاره
                length = np.hypot(index_x - thumb_x, index_y - thumb_y)
                
                # تبدیل فاصله به محدوده صدای سیستم
                vol = np.interp(length, [20, 200], [minVol, maxVol])
                volBar = np.interp(length, [20, 200], [400, 150])
                volPer = np.interp(length, [20, 200], [0, 100])
                
                # تنظیم صدای سیستم
                volume.SetMasterVolumeLevel(vol, None)
                
                # نمایش درصد صدا
                cv2.putText(image, f'Volume: {int(volPer)} %', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                cv2.rectangle(image, (50, 150), (85, 400), (0, 255, 0), 2)
                cv2.rectangle(image, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        
        # نمایش تصویر
        cv2.imshow('Hand Volume Control', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
