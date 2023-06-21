# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:57:00 2022

@author: User
"""
import tkinter as tk
import logging
import cv2
import numpy as np
from djitellopy import Tello #tello
from time import sleep

# 摄像头设置 
Camera_Width = 900
Camera_Height = 600
deadZone =100
startCounter=0
################
Drone = Tello()  # 創建飛行器對象Drone = tello.Tello()
Drone.connect()  # 連接至飛行器
Drone.for_back_velocity = 0
Drone.left_right_velocity = 0
Drone.up_down_velocity = 0
Drone.yaw_velocity = 0
Drone.speed = 0
Drone.streamoff() #重新啟動鏡頭
Drone.streamon()  # 開啟鏡頭傳輸
Drone.LOGGER.setLevel(logging.ERROR)  # 只顯示錯誤訊息
sleep(5)  #  等待鏡頭初始化
print("5秒後鏡頭初始化...")        # 在console輸出 "鏡頭5秒後啟動"
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
            if area >800:#數字越小鎖定距離越遠
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
                        sleep(0.016)
                    elif (cx > int(Camera_Width / 2) + deadZone):
                        cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2+deadZone),int(Camera_Height/2-deadZone)),(Camera_Width,int(Camera_Height/2)+deadZone),(0,0,255),cv2.FILLED)
                        dir = 2
                        sleep(0.016)
                    elif (cy < int(Camera_Height / 2) - deadZone):
                        cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2-deadZone),0),(int(Camera_Width/2+deadZone),int(Camera_Height/2)-deadZone),(0,0,255),cv2.FILLED)
                        dir = 3
                        sleep(0.016)
                    elif (cy > int(Camera_Height / 2) + deadZone):
                        cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                        cv2.rectangle(imgContour,(int(Camera_Width/2-deadZone),int(Camera_Height/2)+deadZone),(int(Camera_Width/2+deadZone),Camera_Height),(0,0,255),cv2.FILLED)
                        dir = 4
                        sleep(0.016)
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
    
    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#輪廓參數
    lower = np.array([133,15,0])#可改參數
    upper = np.array([191,255,255])#可改參數
    mask = cv2.inRange(img_cvt,lower,upper)#可改參數
    result = cv2.bitwise_and(img,img, mask = mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img_blur = cv2.GaussianBlur(result, (7, 7), 1)
    img_gray=cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 166, 171)
    kernel = np.ones((5, 5))
    img_dil = cv2.dilate(img_canny, kernel, iterations=1)
    
    getContours(img_dil, imgContour)
    
    ################# FLIGHT
    if startCounter == 0:
        Drone.takeoff()  #起飛測試時用，須先進行鏡頭測試OK 頂多全部重啟
        sleep(1)
        startCounter = 1     
    if dir == 1:     #GO LEFT
        Drone.left_right_velocity = -45
    elif dir == 2:   #GO RIGHT
        Drone.left_right_velocity = 45
    elif dir == 3:   #GO UP
      Drone.up_down_velocity= 45
    elif dir == 4:   #GO DOWN
      Drone.up_down_velocity= -60
    else:
      Drone.left_right_velocity = 0; Drone.for_back_velocity = 0;Drone.up_down_velocity = 0; Drone.yaw_velocity = 0
    # SEND VELOCITY VALUES TO TELLO
    if Drone.send_rc_control:
      Drone.send_rc_control(Drone.left_right_velocity, Drone.for_back_velocity, Drone.up_down_velocity,Drone.yaw_velocity)
    print(dir)
   ################## FLIGHT
    cv2.imshow('Tello', imgContour)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        Drone.land()
        break

cv2.destroyAllWindows()