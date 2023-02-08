#! /usr/bin/env python3

import Function_Library as LiDAR
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node("RPLiDAR_sensing")

    # Publisher from lidar to master
    direction_pub = rospy.Publisher('/lidar_direction', String, queue_size=1)
    direction = "GO"

    env = LiDAR.libLIDAR('/dev/ttyUSB0')
    env.init()

    env.getState()

    count = 0

    for scan in env.scanning():
        left = env.getAngleDistanceRange(scan, 280, 300, 0, 1300)
        # left2 = env.getAngleDistanceRange(scan, 0, 10, 600, 1000)

        # go = env.getAngleDistanceRange(scan, 10, 60, 0, 400)
        # right = env.getAngleDistanceRange(scan, 11, 150, 0, 550)
        # go2 = env.getAngleDistanceRange(scan, 61, 120, 0, 400)

        if len(left) and count == 0:
            count += 1
            direction = "obstacle"
        else:
            direction = "NO"    # have to change "NO"
        
        direction_pub.publish(direction)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass