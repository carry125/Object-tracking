# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:01:16 2022

@author: User
"""
import cv2
import numpy as np
frameWidth = 640  # WIDTH OF THE IMAGE
frameHeight = 480  # HEIGHT OF THE IMAGE
deadZone =100
cap = cv2.VideoCapture(0)
while True:                    #以下迴圈可以撥放影片
    ret, frame = cap.read()    #一幀一幀讀
    if ret:
        imgcontours = frame.copy()
        frame_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #輪廓參數
        lower = np.array([92,86,191])#可改參數
        upper = np.array([179,122,253])#可改參數
        mask = cv2.inRange(frame_cvt,lower,upper)#可改參數
        result = cv2.bitwise_and(frame,frame, mask = mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        frame_blur = cv2.GaussianBlur(result, (7, 7), 1)
        frame_gray=cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
        frame_canny = cv2.Canny(frame_blur, 166, 171)#可改參數
        kernel = np.ones((5, 5))
        frame_dil = cv2.dilate(frame_canny, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(frame_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:              
                area = cv2.contourArea(cnt)     #print輪廓面積
                if area > 500:
                    cv2.drawContours(imgcontours, cnt, -1, (255,0,255), 7) #在邊界描線
                    peri = cv2.arcLength(cnt, True)  #print輪廓邊長，其中布林值表開放(false)或閉合(true)
                    vertices = cv2.approxPolyDP(cnt, peri*0.02, True) # peri0.02為近似值，愈大多邊形邊愈多，反之亦然。
                    corners = len(vertices)
                    x, y, w, h = cv2.boundingRect(vertices)
                    cx = int(x + (w / 2))  # CENTER X OF THE OBJECT
                    cy = int(y + (h / 2))  # CENTER X OF THE OBJECT     
                              
                    if (cx <int(frameWidth/2)-deadZone):
                            cv2.putText(imgcontours, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                            cv2.rectangle(imgcontours,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                            dir = 1
                    elif (cx > int(frameWidth / 2) + deadZone):
                            cv2.putText(imgcontours, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                            cv2.rectangle(imgcontours,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                            dir = 2
                    elif (cy < int(frameHeight / 2) - deadZone):
                            cv2.putText(imgcontours, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                            cv2.rectangle(imgcontours,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
                            dir = 3
                    elif (cy > int(frameHeight / 2) + deadZone):
                            cv2.putText(imgcontours, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                            cv2.rectangle(imgcontours,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
                            dir = 4
                    else: dir=0
                    cv2.rectangle(imgcontours, (x, y), (x+w, y+h), (0, 255, 0), 4)
                    cv2.putText(imgcontours, 'circle', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255, 2))
                    cv2.line(imgcontours, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),(0, 0, 255), 3)                    
                else: dir=0
        cv2.imshow('video',imgcontours)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
