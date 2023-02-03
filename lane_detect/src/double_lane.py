#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import enum
import numpy as np 
import random
import rospy
from std_msgs.msg import String

def double_lane():
    direction_pub = rospy.Publisher('camera_direction', String, queue_size=1)

    width = 640
    height = 360


    cap = cv2.VideoCapture(0)              
    cap.set(3,width)           #크롭사이즈
    cap.set(4,height)

    #----------------------------
    brightness=20
    contrast=50
    saturation=20
    gain=20
    DETECT_VALUE = 150   #상대밝기
    #----------------------------

    cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)    #카메라조도세팅
    cap.set(cv2.CAP_PROP_CONTRAST,contrast)
    cap.set(cv2.CAP_PROP_SATURATION,saturation)
    cap.set(cv2.CAP_PROP_GAIN,gain)



    min_x = 250               # 인식범위 사이즈
    min_y = 150
    
    direction = "GO"

    while True : 
        
        ret, frame = cap.read()

        max_x = width - min_x
        max_y = height - min_y
        
            
        limited_polylines_list = [[min_x, max_y],  [max_x,max_y], [max_x, min_y], [min_x, min_y]]
        limited_polylines_list_1 = [[min_x-2, max_y+2],  [max_x+2, max_y+2], [max_x+2, min_y-2], [min_x-2, min_y-2]]

        pts = np.array(limited_polylines_list_1, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame, [pts],True, (0, 255, 0), 2)
        cv2.putText(frame, direction, (290,140), cv2.FONT_ITALIC, 1, (0,255,0), 2)
        cv2.imshow("1_polylines",frame)
        
        
        matSrc = np.float32(limited_polylines_list)
        matDst = np.float32([[0,height], [width,height], [width,0], [0,0]])
        matAffine = cv2.getPerspectiveTransform(matSrc,matDst)
        limited_frame = cv2.warpPerspective(frame,matAffine,(width,height))

        gray_frame = cv2.cvtColor(limited_frame, cv2.COLOR_RGB2GRAY)   
        
        dst_retval, dst_binaryzation = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)  
        dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)   
        

        cv2.imshow("dst_binaryzation",dst_binaryzation)              #차선인식
        

        histogram = list(np.sum(dst_binaryzation[:, :], axis=0)) 
        histogram_length = len(histogram)
    
        left = int(np.sum(histogram[:int(histogram_length/4)]))
        mid_left = int(np.sum(histogram[int(histogram_length/4):int(2*histogram_length/4)]))
        mid_right = int(np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)]))
        mid = int(np.sum(histogram[int(1*histogram_length/4):int(3*histogram_length/4)]))
        right = int(np.sum(histogram[int(3*histogram_length/4):]))

        if min_x < 200 : # 최대너비
            min_x = 200

        if min_x > 270 : #최소너비
            min_x = 270

        
        rospy.init_node('direction_publisher')

        # print("LEFT :", left,          "MID :", mid,          "RIGHT : ", right)

    #구간에 안들어가는 곳 체크하기

        if mid < 50000:     #가운데가 검은색일때 : 직진
            if left > 10000000 and right > 10000000 :   #직진
                min_x += 1
                
                direction = "GO"
                print ("           [[ GO ]]:" , left, "     ", mid, "     ", right)
                
                
            else :     #전체가 인식안될때 : 좌우 인식 사이즈 넓히기
                min_x += -1
                # print("--------[[ size re-arrange... ]]--------")
                # print ("min_x :", min_x)
                
        else :     #가운데 흰색일때 : 좌회전 or 우회전
            min_x += 1
            if abs(left-right) < 200000 :     #좌우비슷 : 정지선
                direction = "STOP"
                print ("          [[ STOP ]]:" , abs(left-right))

            else :
                if mid_right - mid_left > 300000 and right - left > 300000 :     #좌회전
                    direction = "LEFT"
                    print ("[[ LEFT ]]:" , mid_right - mid_left)
                    
                if mid_left - mid_right > 300000 and left - right > 300000 :     #우회전
                    direction = "RIGHT"
                    print ("[[ RIGHT ]]:" , mid_right - mid_left)
                # else :     #우회전
                #     direction = "STOP"
                #     print ("          [[ STOP ]]:" , abs(left-right))

        direction_pub.publish(direction)


        k = cv2.waitKey(30) & 0xff   # ESC누르면 종료
        if k == 27: 
            break

    print("------------[SHUT DOWN]------------")

    Stop()
    cap.release()

    exit()


double_lane()