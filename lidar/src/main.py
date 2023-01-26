#! /usr/bin/env python3

import Function_Library as LiDAR
import rospy

def main():
    rospy.init_node("RPLiDAR_sensing")

    env = LiDAR.libLIDAR('/dev/ttyUSB0')
    env.init()

    env.getState()

    count = 0

    no_obstacle = True

    while no_obstacle : 
        for scan in env.scanning():
            scan = env.getAngleDistanceRange(scan, 0, 30, 0, 300)
            count += 1

            if len(scan):
                print(scan)

            if count == 100:
                env.stop()
                no_obstacle = False
                break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass