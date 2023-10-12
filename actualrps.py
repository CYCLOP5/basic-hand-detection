import cv2 as cv
import mediapipe as mp
#21 POINT
#https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
debug = False
video = cv.VideoCapture(0)#goofy ahh shit dont work dawg

#remember : in a cv frame y downwards means increasing and x rightwards means increasing

def getHandMovement(hand_landmarks):#only works on specific angle
    landmarks = hand_landmarks.landmark #represnt the particular point XYZ
    if all([landmarks[i].y<landmarks[i+3].y for i in range(5,20,4)]) :#landmarks at any I pos is offset at 3
        return "Rock"#top landmakrs will touch  red points 
    elif landmarks[13].y<landmarks[16].y and landmarks[17].y<landmarks[20].y:#landmark 13 below 16 and 17 below 20
        return "scisor"
    else:
        return "paper"  
    
internalclock=0
player1_move=player2_move=None
text=""
checkFor2hands=True


with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:#never change var names shit is reserved
    

    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            break
        #FRAME ALWAYS COMES TO BGR SO WE MUST CHANGE ig 
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) #colour change up to RGB
        results = hands.process(frame) #get them hand
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)#revert to og colour space aka BGR
        if results.multi_hand_landmarks: #just check null
            for hand_landmarks in results.multi_hand_landmarks: #go through array list to check (no of hands in frames) 
                mp_drawing.draw_landmarks(frame, #once again never change var names shit is reserved
                                      hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS,
                                      mp_drawing_styles.get_default_hand_landmarks_style(),
                                      mp_drawing_styles.get_default_hand_connections_style())#draw default colours on hands
        frame = cv.flip(frame,1)#for some reason cam is flipped idk its just to get mirror image 

        if 0<= internalclock<20:
            checkFor2hands= True
            text ="ready"
        elif internalclock<50:
            text="3"
        elif internalclock<70:
            text="2"
        elif internalclock<90:
            text="1"
        elif internalclock<110:
            text="show them hands"
        elif internalclock==110:
            handdetect = results.multi_hand_landmarks 
            if handdetect and len(handdetect)==2:#check if not null and check if there are 2 hand
                player1_move = getHandMovement(handdetect[0])
                player2_move = getHandMovement(handdetect[1])#somtimes can flip p1 and p2 @rahul help
            else:
                    checkFor2hands=False
        elif internalclock<200:
            if checkFor2hands:
                if debug==True:
                        print(player1_move,player2_move)
                if player1_move == player2_move:
                    text="draw"
                elif player1_move == "Rock" and player2_move == "scisor":
                    text="player 1 wins"
                elif player1_move == "scisor" and player2_move == "paper":
                    text="player 1 wins"
                elif player1_move == "paper" and player2_move == "Rock":
                    text="player 1 wins"
                else:
                    text="player 2 wins"
            else:
                text="blud u need 2 ppl or 2 hands"

        cv.putText(frame,text,(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv.LINE_AA)
        cv.putText(frame,"player 1: "+str(player1_move),(50,100),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv.LINE_AA)
        cv.putText(frame,"player 2: "+str(player2_move),(50,150),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv.LINE_AA)
        cv.putText(frame,"framecount: "+str(internalclock),(50,200),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv.LINE_AA)
        internalclock=(internalclock+1)%250#repeat every 250frames
        cv.imshow('cams on woo', frame)
        if cv.waitKey(1)&0xff == ord('c'):
            break
video.release()
cv.destroyAllWindows()