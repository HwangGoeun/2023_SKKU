#! /usr/bin/env python3

import Function_Library as LiDAR
import rospy
from std_msgs.msg import String
from time import time

def main():
    rospy.init_node("RPLiDAR_sensing")

    # Publisher from lidar to master
    direction_pub = rospy.Publisher('/lidar_direction', String, queue_size=1)
    direction = "GO"

    env = LiDAR.libLIDAR('/dev/ttyUSB0')    #lidar parameter
    env.init()

    env.getState()

    delay = 5
    obstacle = 0
    first_time = 0

    for scan in env.scanning(): #lidar sacn start
        left = env.getAngleDistanceRange(scan, 280, 300, 0, 1300)   #lidar scan range (getAngleDistanceRange(self, scan, minAngle, maxAngle, minDist, maxDist):)
        
        if len(left) and obstacle < 2:  #obstacle detected
            if obstacle == 0:
                direction = "obstacle1" #change direction "obstacle1"
                print("obstacle 1")
                obstacle += 1
                first_time = time.time()

            if obstacle:
                cur_time = time.time()  #check obstacle detection time

            if cur_time - first_time > delay:   #After 5s detecting obstacle
                if len(left):
                    direction = "obstacle 2"    #change direction "obstacle 2"
                    print("obstacle 2")
                    obstacle += 1
        else:
            direction = "NO"    # have to change "NO"
        
        direction_pub.publish(direction)    #publish direction message

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass