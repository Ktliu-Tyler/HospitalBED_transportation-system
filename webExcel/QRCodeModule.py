import time
import cv2
import numpy as np
import os
from pyzbar.pyzbar import decode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class MakeQRCode:
    def __init__(self):
        self.data = ''
        self.driver = None
        self.url = ''

    def setUrl(self, url='https://www.the-qrcode-generator.com/'):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = url

    def sendData(self, data):
        time.sleep(1)
        text = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[3]/div/div/div/textarea[1]')
        text.clear()
        self.data = data
        text.send_keys(data)

    def runMultipleQRCodes(self, multipleData, filePath, isClose=True):
        self.setUrl()
        self.multipleData = multipleData
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        fileList = os.listdir(filePath)
        self.driver.get(self.url)
        waitBtn = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[2]/div/div/div/div/input')
        time.sleep(1)
        toTextButton = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[1]/div/div[3]/div/button[2]')
        toTextButton.click()

        for data in self.multipleData:
            if not f"{data}.png" in fileList:
                text = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[3]/div/div/div/textarea[1]')
                self.data = data
                text.send_keys(data)
                images = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/canvas')
                images.screenshot(f'{filePath}/{data}.png')
                text.send_keys(Keys.CONTROL + "a")
                text.send_keys(Keys.DELETE)

        time.sleep(2)
        if isClose:
            self.driver.quit()

    def runDefault(self, data, filePath, isClose=True):
        self.setUrl()
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        self.driver.get(self.url)
        waitBtn = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[2]/div/div/div/div/input')
        time.sleep(1)
        waitBtn.clear()
        toTextButton = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[1]/div/div[3]/div/button[2]')
        toTextButton.click()

        time.sleep(1)
        text = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[1]/div[3]/div/div/div/textarea[1]')
        text.clear()
        self.data = data
        text.send_keys(data)
        images = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/canvas')
        images.screenshot(f'{filePath}/{data}.png')

        time.sleep(2)
        if isClose:
            self.driver.quit()


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

    def decodeQRCode(self, frame, showText=True):
        myData = ''
        for barcode in decode(frame):
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, self.color, 3)
            pts2 = barcode.rect
            myData = barcode.data.decode('utf-8')
            if showText:
                cv2.putText(frame, myData, (pts2[0], pts2[1]),
                            cv2.FONT_ITALIC, 1.2, self.color, 2)

        return myData, frame

    def runDefault(self):
        while True:
            timer = cv2.getTickCount()
            ret, frame = self.cap.read()
            result, frame = self.decodeQRCode(frame)
            print(result)

            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            cv2.putText(frame, f'FPS: {int(fps)}', (20, 40), cv2.FONT_ITALIC, 1.2, (255, 0, 255), 2)
            cv2.imshow('Image', frame)

            if cv2.waitKey(1) & 0xFF == ord(' '):
                self.cap.release()
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    # maker = MakeQRCode()
    # maker.setUrl()
    # maker.runDefault('A153232928', './')
    qrcoder = QRCodeScanner()
    qrcoder.runDefault()

