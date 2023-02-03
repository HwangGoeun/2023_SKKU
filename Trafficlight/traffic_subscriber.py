#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import enum
import numpy as np 
import random
import rospy
from std_msgs.msg import String

def callback(msg):
    print(msg.data)
    
rospy.init_node('traffic_subscriber')
sub = rospy.Subscriber('color', String, callback)
rospy.spin()