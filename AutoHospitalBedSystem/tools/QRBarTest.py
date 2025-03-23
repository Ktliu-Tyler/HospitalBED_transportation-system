import cv2
import os
import numpy as np
from pyzbar.pyzbar import decode


###########################################
wCam, hCam = 640, 480
###########################################


file = os.listdir('QRCode')
listImg = []
for f in file:
    img = cv2.imread(f'QRCode/{f}')
    listImg.append(img)

# print(len(listImg))


# code = decode(listImg[0])
# for i in range(len(listImg)):
#     for barcode in decode(listImg[i]):
#         print(barcode.data)
#         myData = barcode.data.decode('utf-8')
#         print(myData)

# print(code)


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(10, 150)


while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()

    for barcode in decode(frame):
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (255, 0, 255), 3)
        pts2 = barcode.rect
        myData = barcode.data.decode('utf-8')
        cv2.putText(frame, myData, (pts2[0], pts2[1]),
                    cv2.FONT_ITALIC, 1.2, (255, 0, 255), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 40), cv2.FONT_ITALIC, 1.2, (255, 0, 255), 2)
    cv2.imshow('Image', frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        cap.release()
        cv2.destroyAllWindows()
        break

