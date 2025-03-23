# from MotorModule import Motor
from LaneDetectionModule import LaneDetection
from tools import utlis
import WebcamModule
import cv2


#############################################
# motor = Motor(2, 3, 4, 17, 22, 27)
#############################################


def main():
    lane = LaneDetection()
    frame = WebcamModule.getImg()
    initialTrackBarVals = [102, 80, 20, 214]
    utlis.initializeTrackbars(initialTrackBarVals)
    # lane.main()
    curveVal = lane.getLaneCurve(frame, 1)

    sen = 1.3  # SENSITIVITY
    maxVal = 0.3  # MAX SPEED
    if curveVal > maxVal:
        curveVal = maxVal
    if curveVal < -maxVal:
        curveVal = -maxVal
    # print(curveVal)
    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05:
            curveVal = 0
    else:
        if curveVal > -0.08:
            curveVal = 0
    # motor.move(0.20, -curveVal*sen, 0.05)
    cv2.imshow('Frame', frame)


if __name__ == "__main__":
    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cap.release()
            cv2.destroyAllWindows()
            break

