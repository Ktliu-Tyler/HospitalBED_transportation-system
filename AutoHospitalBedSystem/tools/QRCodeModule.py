import cv2
import numpy as np
from pyzbar.pyzbar import decode


class QRCodeScanner:
    def __init__(self, winSize=(320, 320), cameraNo=0, brightness=100, innerCapture=True):
        self.width = winSize[0]
        self.height = winSize[1]
        self.cameraNo = cameraNo
        self.brightness = brightness
        if innerCapture:
            self.cap = cv2.VideoCapture(self.cameraNo)
            self.cap.set(3, self.width)
            self.cap.set(4, self.height)
            self.cap.set(10, self.brightness)
            self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.color = (255, 0, 255)

    def decodeQRCode(self, frame):
        myData = ''
        for barcode in decode(frame):
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, self.color, 3)
            pts2 = barcode.rect
            myData = barcode.data.decode('utf-8')

            cv2.putText(frame, myData, (pts2[0], pts2[1]),
                        cv2.FONT_ITALIC, 1.2, self.color, 2)

        return myData, frame


if __name__ == "__main__":
    qrcode = QRCodeScanner()
    while True:
        timer = cv2.getTickCount()
        ret, frame = qrcode.cap.read()
        result, frame = qrcode.decodeQRCode(frame)
        print(result)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 40), cv2.FONT_ITALIC, 1.2, (255, 0, 255), 2)
        cv2.imshow('Image', frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            qrcode.cap.release()
            cv2.destroyAllWindows()
            break
