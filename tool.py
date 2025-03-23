from PIL import Image, ImageTk
import cv2
import threading
import tkinter as tk
import pickle


class Capture:
    def __init__(self, capNum):
        self.Frame = []
        self.status = False
        self.isstop = False
        self.capNum = capNum

    def start(self):
        print('Camera started!')
        self.cap = cv2.VideoCapture(self.capNum)
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('Camera stopped!')

    def getframe(self):
        return self.status, self.Frame.copy()

    def imshow(self, name, img):
        if self.status:
            cv2.imshow(name, img)

    def getKey(self):
        return cv2.waitKey(1)

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.cap.read()
        self.cap.release()
        cv2.destroyAllWindows()


class Bed:
    def __init__(self, c, addr, name):
        self.client = c
        self.addr = addr
        self.name = name
        self.is_pos = False
        self.is_r_img = False
        self.is_p_img = False
        self.is_append = False
        self.pos = None

    def get_Rimg(self, img):
        self.route_img = img
        self.is_r_img = True

    def get_Pimg(self, img):
        self.patient_img = img
        self.is_p_img = True

    def get_pos(self, pos):
        self.pos = pos
        self.is_pos = True

    def is_complete(self):
        if self.is_pos and self.is_r_img and self.is_p_img:
            return True
        else:
            return False


def process_image(img):  # 影像前置處理
    img = cv2.resize(img, (400, 300))
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk

def process_patient_image(img):  # 影像前置處理
    while img.shape[1] > 320:
        img = cv2.resize(img, (int(img.shape[1]*0.8), int(img.shape[0]*0.8)))
    img = img[20: img.shape[0], 30: img.shape[1]-30]
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk

