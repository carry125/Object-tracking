# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!!!!聯外防火牆需要關閉!!!!
import logging
import time
import cv2
from djitellopy import tello
from time import sleep
# 摄像头设置 
Camera_Width = 720
Camera_Height = 480
DetectRange = [6000, 11000]  # DetectRange[0] 是保持静止的检测人脸面积阈值下限，DetectRange[0] 是保持静止的检测人脸面积阈值上限
PID_Parameter = [0.5, 0.0004, 0.4]
pErrorRotate, pErrorUp = 0, 0

# 字体设置
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (255, 0, 0)
lineThickness = 1

# Tello初始化设置
Drone = tello.Tello()  # 创建飞行器对象
Drone.connect()  # 连接到飞行器
Drone.streamon()  # 开启视频传输
Drone.LOGGER.setLevel(logging.ERROR)  # 只显示错误信息
sleep(5)  #  等待视频初始化


while True:
    OriginalImage = Drone.get_frame_read().frame
    Image = cv2.resize(OriginalImage, (Camera_Width, Camera_Height))
    cv2.imshow("Drone Control Centre", Image)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        Drone.streamoff()
        break
