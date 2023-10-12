import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

video = cv.VideoCapture(0)#goofy ahh shit dont work dawg


with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:#never change var names shit is reserved
    

    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            break
        
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) #colour change up to RGB
        results = hands.process(frame) #get them thicc hand
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)#colour change up to BGR
        if results.multi_hand_landmarks: #just check null
            for hand_landmarks in results.multi_hand_landmarks: #go through array list to check 
                mp_drawing.draw_landmarks(frame, #once again never change var names shit is reserved
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      mp_drawing_styles.get_default_hand_landmarks_style(),
                                      mp_drawing_styles.get_default_hand_connections_style())#draw default colours on hands
        frame = cv.flip(frame,1)#for some reason cam is flipped idk
        cv.imshow('cams on woo', frame)
        if cv.waitKey(1)&0xff == ord('c'):
            break
video.release()
cv.destroyAllWindows()