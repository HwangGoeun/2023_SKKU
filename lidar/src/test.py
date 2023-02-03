import Lib_LiDAR as LiDAR

if __name__ == '__main__':
    env = LiDAR.libLIDAR('COM17')
    env.init()

    env.getState()

    count = 0

    for scan in env.scanning():
        count += 1

        left = env.getAngleDistanceRange(scan, 0, 30, 0, 400)
        go = env.getAngleDistanceRange(scan, 31, 120, 0, 300)
        right = env.getAngleDistanceRange(scan, 121, 180, 400, 800)

        if len(left):
            print("left")
        else:
            if len(go):
                print("go")
            else:
                if len(right):
                    print("right")
                else:
                    print("")


        if count == 500:
            env.stop()
            break