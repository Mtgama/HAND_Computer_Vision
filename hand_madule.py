import cv2
import mediapipe as mp 

class Detector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mediapipeHands = mp.solutions.hands 
        self.hands = self.mediapipeHands.Hands(static_image_mode=self.mode, 
                                               max_num_hands=self.maxHands,
                                               min_detection_confidence=self.detectionCon, 
                                               min_tracking_confidence=self.trackingCon)
        self.Draw = mp.solutions.drawing_utils

    def findhands(self, frame, draw=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(frameRGB)
        if self.result.multi_hand_landmarks:
            for handlandmarks in self.result.multi_hand_landmarks:
                if draw:
                    self.Draw.draw_landmarks(frame, handlandmarks, self.mediapipeHands.HAND_CONNECTIONS)
        return frame

    def Position(self, frame, handNo=0, draw=True):
        landmarkList = []
        if self.result.multi_hand_landmarks:
            myHands = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = frame.shape
                x, y = int(lm.x * w), int(lm.y * h)
                landmarkList.append([id, x, y])
                if draw:
                    cv2.circle(frame, (x, y), 8, (255, 0, 0), -1)
        return landmarkList

def main():
    cap = cv2.VideoCapture(0)
    detector = Detector()
    while True:
        _, frame = cap.read()
        detector.findhands(frame)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()
