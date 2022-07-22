# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:57:00 2022

@author: User
"""
import logging
import cv2
from djitellopy import tello
from time import sleep

# 摄像头设置 
Camera_Width = 720
Camera_Height = 480
deadZone =100
################
Drone = tello.Tello()  # 創建飛行器對象
Drone.connect()  # 連接至飛行器
Drone.streamoff() #重新啟動鏡頭
Drone.streamon()  # 開啟鏡頭傳輸
Drone.LOGGER.setLevel(logging.ERROR)  # 只顯示錯誤訊息
sleep(5)  #  等待鏡頭初始化
################
#全域參數設置
global imgContour
global dir;
def empty(a):
    pass
################


################
def getContours(img,imgContour):
        global dir
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)     #print輪廓面積
            if area > 500:#數字越小鎖定距離越遠
                cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7) #在邊界描線
                peri = cv2.arcLength(cnt, True)  #print輪廓邊長，其中布林值表開放(false)或閉合(true)
                vertices = cv2.approxPolyDP(cnt, peri*0.02, True)
                corners = len(vertices)
                x, y, w, h = cv2.boundingRect(vertices)
                cx = int(x + (w / 2))  # CENTER X OF THE OBJECT
                cy = int(y + (h / 2))  # CENTER X OF THE OBJECT
                if corners >= 8:
                    if (cx <int(Camera_Width/2)-deadZone):
                        cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(0,int(Camera_Height/2-deadZone)),(int(Camera_Width/2)-deadZone,int(Camera_Height/2)+deadZone),(0,0,255),cv2.FILLED)
                        dir = 1
                    elif (cx > int(Camera_Width / 2) + deadZone):
                        cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2+deadZone),int(Camera_Height/2-deadZone)),(Camera_Width,int(Camera_Height/2)+deadZone),(0,0,255),cv2.FILLED)
                        dir = 2
                    elif (cy < int(Camera_Height / 2) - deadZone):
                        cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2-deadZone),0),(int(Camera_Width/2+deadZone),int(Camera_Height/2)-deadZone),(0,0,255),cv2.FILLED)
                        dir = 3
                    elif (cy > int(Camera_Height / 2) + deadZone):
                        cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2-deadZone),int(Camera_Height/2)+deadZone),(int(Camera_Width/2+deadZone),Camera_Height),(0,0,255),cv2.FILLED)
                        dir = 4
                    else: dir=0
                    cv2.line(imgContour, (int(Camera_Width/2),int(Camera_Height/2)), (cx,cy),(0, 0, 255), 3)
            else: dir=0
           #到此皆為辨識與追蹤用                              
################
while True:
    frame_read = Drone.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (Camera_Width, Camera_Height))
    imgContour=img.copy()#用imgContour輸出畫面楨
    imgblur = cv2.GaussianBlur(img, (3, 3), 0)
    imgcanny = cv2.Canny(imgblur, 100, 150)
    getContours(imgcanny, imgContour)
    cv2.imshow('Tello', imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break