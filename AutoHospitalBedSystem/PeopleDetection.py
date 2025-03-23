import threading
import cv2
import numpy as np
# from tools import musicPlayer as mu
from .tools import musicPlayer as mu
# from AutoHospitalBedSystem.tools import LaneDetectionModule as ldm
# from tools import utlis
# from module import MotorModule as mmd
# from tools import LaneDetectionModule as ldm
# from tools import QRCodeModule


class yoloDetect:

    def __init__(self, yolo_mode='tiny', conf=0.8, nms_conf=0.6, GPU=True):
        """
            :param yolo_mode: chose model with tiny or 320 version
            :param conf: set detection confidence
            :param nms_conf: set NMS confidence
            :param GPU: use gpu or cpu
        """

        if yolo_mode == 'tiny':

            self.modelConfiguration = r'C:\Users\Liu Ty\Desktop\All python\Project\Hospital_Bed\newHospitalBed\AutoHospitalBedSystem\Resources\yolov3-tiny.cfg'
            self.modelWeight = r'C:\Users\Liu Ty\Desktop\All python\Project\Hospital_Bed\newHospitalBed\AutoHospitalBedSystem\Resources\yolov3-tiny.weights'
        else:
            self.modelConfiguration = r'C:\Users\Liu Ty\Desktop\All python\Project\Hospital_Bed\newHospitalBed\AutoHospitalBedSystem\Resources\yolov3-320.cfg'
            self.modelWeight = r'C:\Users\Liu Ty\Desktop\All python\Project\Hospital_Bed\newHospitalBed\AutoHospitalBedSystem\Resources\yolov3-320.weights'

        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeight)
        if GPU:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.conf = conf
        self.nms_conf = nms_conf

        # Variable Area
        ################################################
        self.sound = mu.Sound()
        self.whT = 320
        self.classesFile = r'C:\Users\Liu Ty\Desktop\All python\Project\Hospital_Bed\newHospitalBed\AutoHospitalBedSystem\Resources\coco.names'
        self.classes = []

        self.thread = None
        self.func = None
        self.args = []
        with open(self.classesFile, 'rt') as f:
            self.className = f.read().rstrip('\n').split('\n')

    def setThread(self, func, args:list):
        """
        To set the function what you want to do in yoloDetect.warning function
        :param func: pass the function you want thread to do
        :param args: your function parameters
        :return:
        """
        # self.thread = threading.Thread(target=func, args=args)
        self.func = func
        self.args = args

    def findObjects(self, outputs, img):
        """
        To find the person class detection

        """
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
        findPerson = False

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if (confidence > self.conf) and self.className[classId] == 'person':
                    w, h = int(det[2]*wT), int(det[3]*hT)
                    x, y = int(det[0]*wT - w/2), int(det[1]*hT - h/2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))
                    findPerson = True

        if findPerson:
            # print(len(bbox))
            indices = cv2.dnn.NMSBoxes(bbox, confs, self.conf, self.nms_conf)
            for i in indices:
                box = bbox[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, f'{self.className[classIds[i]].upper()} {int(confs[i]*100)} %',
                            (x, y-10), cv2.FONT_ITALIC, 0.6, (0, 255, 0), 2)

        return bbox, classIds, confs, findPerson

    def getDefaultOut(self, frame):
        """
        You can simply call this function to get People Detection
        :param frame: pass cv2 image to process
        :return: return find person or not, and also return processed image
        """
        # ret, frame = cap.read()

        timer = cv2.getTickCount()
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (self.whT, self.whT), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)

        layerNames = self.net.getLayerNames()
        # print(layerNames)
        #
        # print(self.net.getUnconnectedOutLayers())
        # for i in self.net.getUnconnectedOutLayers():
        #     # print(type(i), i)
        #     print(layerNames[i - 1])
        outputNames = [layerNames[i - 1] for i in self.net.getUnconnectedOutLayers()]
        # print(outputNames)

        outputs = self.net.forward(outputNames)
        # print(len(outputs))
        # print(outputs[0].shape)
        # print(outputs[1].shape)
        # print(outputs[2].shape)
        # print(outputs[0][0])

        bbox, classIds, confs, findPerson = self.findObjects(outputs, frame)

        fps = cv2.getTickFrequency() // (cv2.getTickCount() - timer)
        cv2.putText(frame, f'FPS: {int(fps)}', (25, 35), cv2.FONT_ITALIC, 1.2, (255, 0, 255), 2)

        return bbox, classIds, confs, findPerson, frame

    def warning(self):
        if self.thread == None:
            self.thread = threading.Thread(target=self.func, args=self.args)
            self.thread.start()
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.func, args=self.args)
            self.thread.start()
        # self.sound.playSound(path, epochs, volume)
        # pTime = time.time()

        # thread.join()  // wait until the function has done

        # print('Do not stand here!!!')

    def safe(self):
        # print('Keep going')
        pass


if __name__ == "__main__":
    musicPath = './Resources/kt.mp3'
    yolo = yoloDetect('320', conf=0.3, nms_conf=0.3, GPU=False)
    cap = cv2.VideoCapture(0)
    yolo.setThread(yolo.sound.play, args=[musicPath, 1, 0.5])
    # cap.set(cv2.CAP_PROP_FPS, 60)
    # QRCode = QRCodeModule.QRCodeScanner(innerCapture=False)
    # motor = mmd.Motor(33, 35, 37, 32, 36, 38, 'BOARD')
    # lane = ldm.LaneDetection()
    # frameCounter = 0
    # initialTrackBarVals = [102, 80, 20, 214]
    # utlis.initializeTrackbars(initialTrackBarVals)
    while True:
        # frameCounter += 1
        # if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #     frameCounter = 0
        ret, frame = cap.read()
        bbox, classIds, confs, findPerson, frame = yolo.getDefaultOut(frame)

        # data, frame = QRCode.decodeQRCode(frame)

        # frame = cv2.resize(frame, (480, 240))
        # curve = lane.getLaneCurve(frame, display=1)
        # print(curve)

        if findPerson:
            yolo.warning()
            pass
        else:
            yolo.safe()

        cv2.imshow('Image', frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            cap.release()
            cv2.destroyAllWindows()
            break



