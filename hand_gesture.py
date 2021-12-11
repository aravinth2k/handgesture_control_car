# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:16:07 2021

@author: Aravinth B
"""

import cv2
import mediapipe as mp
import serial

Video = cv2.VideoCapture(0)
ser = serial.Serial('COM4',9600,timeout=1)
mphand = mp.solutions.hands
hand = mphand.Hands(max_num_hands=2,min_tracking_confidence=0.7)
mpdraw = mp.solutions.drawing_utils

while True:
    
    img ,frame = Video.read()
    h,w,c = frame.shape
    
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hand.process(gray)
    
    if result.multi_hand_landmarks:
        landmarks =  []
        for handlms in result.multi_hand_landmarks:
             thumbx = handlms.landmark[mphand.HandLandmark.THUMB_TIP].x * w
             thumby = handlms.landmark[mphand.HandLandmark.THUMB_TIP].y * h
             
             wristx = handlms.landmark[mphand.HandLandmark.WRIST].x * w
             wristy = handlms.landmark[mphand.HandLandmark.WRIST].y * h
             
             print("thumb",thumbx,thumby)
             print("wrist",wristx,wristy)
             ser.write(b"N")
             if(thumbx > wristx and thumby < wristy):
                 print("Left")
                 ser.write(b"L")
             elif(wristx > thumbx and wristy > thumby):
                 if(wristx-thumbx < 50):
                     print("Up")
                     ser.write(b"U")
                 else:
                     print("Right")
                     ser.write(b"R")
             elif(thumbx > wristx and thumby > wristy):
                 print("Down")
                 ser.write(b"D")
             x_max = 0
             y_max = 0
             x_min = w
             y_min = h
             for lms in handlms.landmark:
                x, y = int(lms.x * w), int(lms.y *h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                lmx = int(lms.x * h)
                lmy = int(lms.y * w)
                landmarks.append([lmx,lmy])
        cv2.rectangle(frame, (x_min-15, y_min-15), (x_max+15, y_max+15), (0, 255, 0), 2)
        mpdraw.draw_landmarks(frame, handlms,mphand.HAND_CONNECTIONS)
    cv2.imshow('capture',frame)
    if cv2.waitKey(1) == ord('q'):
        ser.close()
        break
    
Video.release()
cv2.destroyAllWindows()