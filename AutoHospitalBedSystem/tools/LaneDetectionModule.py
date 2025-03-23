import cv2
import numpy as np
from ..tools import utlis
# import utlis
# from AutoHospitalBedSystem.tools import utlis


class LaneDetection:
    def __init__(self):
        self.curveList = []
        self.avgVal = 10
        self.curve = 0

    def getLaneCurve(self, img, display=2):
        imgCopy = img.copy()
        imgResult = img.copy()
        # # # STEP 1
        imgThres = utlis.thresholding(img)

        # # # STEP 2
        hT, wT, c = img.shape
        points = np.float32([(102, 80), (wT-102, 80),
                      (20 , 214 ), (wT-20, 214)])
        # points = utlis.valTrackbars()
        imgWarp = utlis.warpImg(imgThres, points, wT, hT)
        imgWarpPoints = utlis.drawPoints(imgCopy, points)

        # # # STEP 3
        middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
        curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
        # print(curveAveragePoint-middlePoint)
        curveRaw = curveAveragePoint - middlePoint

        # # # STEP 4
        self.curveList.append(curveRaw)
        if len(self.curveList) > self.avgVal:
            self.curveList.pop(0)
        curve = int(sum(self.curveList)/len(self.curveList))
        # cv2.line()
        # # # STEP 5

        if display != 0:
            imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inverse=True)
            imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
            imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
            imgLaneColor = np.zeros_like(img)
            imgLaneColor[:] = 0, 255, 0
            imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
            imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
            midY = 220
            cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
            cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
            for x in range(-30, 30):
                w = wT // 20
                cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                         (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
            # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
            # cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
        if display == 2:
            imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                                 [imgHist, imgLaneColor, imgResult]))
            cv2.imshow('ImageStack', imgStacked)
        elif display == 1:
            cv2.imshow('Result', imgResult)

        # # # NORMALIZATION
        curve = curve / 100
        if curve > 1:
            curve = 1
        if curve < -1:
            curve = -1
        self.curve = int(curve * 100)
        return curve

    def main(self):
        cap = cv2.VideoCapture(0)
        frameCounter = 0
        initialTrackBarVals = [102, 80, 20, 214]
        utlis.initializeTrackbars(initialTrackBarVals)
        while True:
            frameCounter += 1
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            ret, frame = cap.read()
            frame = cv2.resize(frame, (480, 240))
            curve = self.getLaneCurve(frame, display=1)
            # print(curve)
            # cv2.imshow('Frame', frame)
            if cv2.waitKey(5) & 0xFF == ord(' '):
                cap.release()
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    lane = LaneDetection()
    lane.main()
