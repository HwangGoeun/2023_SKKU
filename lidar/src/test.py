import Lib_LiDAR as LiDAR

if __name__ == '__main__':
    env = LiDAR.libLIDAR('COM17')
    env.init()

    env.getState()

    count = 0

    for scan in env.scanning():
        count += 1

        left = env.getAngleDistanceRange(scan, 330, 360, 800, 1000)
        go = env.getAngleDistanceRange(scan, 0, 40, 0, 400)
        right = env.getAngleDistanceRange(scan, 41, 60, 400, 600)
        go2 = env.getAngleDistanceRange(scan, 61, 120, 0, 400)

        if len(left):
            print("left")
        else:
            if len(go) or len(go2):
                print("go")
            else:
                if len(right):
                    print("right")
                else:
                    print("")


        if count == 500:
            env.stop()
            break