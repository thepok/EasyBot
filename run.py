from robot import Robot
import time


if __name__ == "__main__":
    robot = Robot()
    print("Robot initialized!")

    while True:
        print("Moving all servos...")
        robot.extend(20)
        time.sleep(0.1)

        #print("Moving all servos back...")
        #robot.extend(-20)
        #time.sleep(2)