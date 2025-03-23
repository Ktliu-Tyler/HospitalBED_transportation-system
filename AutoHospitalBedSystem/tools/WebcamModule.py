import cv2


cap = cv2.VideoCapture(1)


def getImg(display=False, size=(480, 240)):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (size[0], size[1]))
    if display:
        cv2.imshow('IMG', frame)
    return frame


if __name__ == "__main__":
    while True:
        img = getImg(True)

