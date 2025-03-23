import socket, cv2, pickle, struct
import pyshine as ps
import imutils
import threading
# import pygame
import time
from AutoHospitalBedSystem import PeopleDetection as People
import serial
from AutoHospitalBedSystem.tools import LaneDetectionModule as ldm
from AutoHospitalBedSystem.tools import utlis


POS = (5,17)
PORT = 9999
class client:
    def __init__(self, y, x, host_ip, port, ArduinoCOM):
        self.Ard = ArduinoCOM
        self.keep_moving = False
        self.if_human = False
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.curve = 0
        self.if_video = True
        self.transporting = False
        self.Close = False
        self.frame1 = cv2.imread("img/hospital.png")
        self.turn = "f" # 誤差偏移方向
        if self.if_video:
            self.vid1 = cv2.VideoCapture(0)
            self.vid2 = cv2.VideoCapture(1)
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_ip = host_ip
        self.port = port
        self.Ard = "COM4"
        self.ADDR = (host_ip,port)
        self.connecting = False
        self.Disconnect = False
        self.threading_list = []
        self.connect_socket()
        self.arduino = self.connect_arduino()
        if not self.Close:
            self.lane = ldm.LaneDetection()
            self.sending()
            self.recving()
            self.path_bool = []
            self.path_dir = []
            self.path_pos = []
            self.yolo = People.yoloDetect('tiny', 0.4, 0.3, GPU=False)
            self.musicPath = 'AutoHospitalBedSystem\Resources\kt.mp3'
            self.yolo.setThread(self.yolo.sound.play, args=[self.musicPath, 1, 0.5])
            self.detecting()

    def connect_socket(self):
        while True:
            try:
                self.client_socket.connect(self.ADDR)
                self.connecting = True
                print("[SOCKET CONNECTED!]")
                break
            except:
                self.host_ip = input("[ADDRESS ERROR!] Can't find the address, please enter again...\n")
                if self.host_ip == " ":
                    self.Close = True
                    break
                self.ADDR = (self.host_ip, self.port)

    def connect_arduino(self):
        while True:
            try:
                arduino = serial.Serial(self.Ard, 9600)
                print("[ARDUINO CONNECTED!]")
                return arduino
            except:
                self.Ard = input("[ARDUINO ERROR!] Can't find the arduino COM, please enter again...\n")
                if self.Ard == " ":
                    self.Close = True
                    break

    def sending(self):
        t = threading.Thread(target=self.sendata)
        t.daemon = True
        self.threading_list.append(t)
        t.start()

    def recving(self):
        t = threading.Thread(target=self.recvdata)
        t.daemon = True
        self.threading_list.append(t)
        t.start()

    def detecting(self):
        t = threading.Thread(target=self.humanDetect)
        t.daemon = True
        self.threading_list.append(t)
        t.start()

    def detectLane(self):
        t = threading.Thread(target=self.lane.getLaneCurve, args=(self.frame1, 2))
        t.daemon = True
        self.threading_list.append(t)
        t.start()

    def sendArdCurve(self):
        print(self.pos)
        message = f'@{self.lane.curve}'
        self.Arduino_send(self.arduino, message)

    def recvdata(self):
        while True:
            if self.connecting:
                try:
                    payload_size = struct.calcsize("3Q")
                    while self.client_socket:
                        data = b""
                        while len(data) < payload_size:
                            packet = self.client_socket.recv(4*1024) # 4K
                            if not packet: break
                            data += packet
                        packed_msg_size = data[:payload_size]
                        data = data[payload_size:]
                        size1 = struct.unpack("3Q",packed_msg_size)[0]
                        size2 = struct.unpack("3Q",packed_msg_size)[1]
                        size3 = struct.unpack("3Q",packed_msg_size)[2]
                        # print(size1,size2)
                        while len(data) < size1:
                            data += self.client_socket.recv(4*1024)
                        path_data = data[:size1]
                        data = data[size1:]
                        path_bool = pickle.loads(path_data)
                        while len(data) < size2:
                            data += self.client_socket.recv(4*1024)
                        path_data = data[:size2]
                        data = data[size2:]
                        path_dir = pickle.loads(path_data)
                        while len(data) < size3:
                            data += self.client_socket.recv(4*1024)
                        path_data = data[:size3]
                        data = data[size3:]
                        path_pos = pickle.loads(path_data)


                        self.path_bool = path_bool
                        self.path_dir = path_dir
                        self.path_pos = path_pos
                        if not(self.transporting):
                            self.transporting = True
                            self.Bed_Transport()
                            print("[START TRANSPORT]")

                except Exception as e:
                    print(e)

    def sendata(self):
        if self.connecting:
            try:
                while True:
                    # print(self.pos)
                    if self.if_video:
                        img, self.frame1 = self.vid1.read()
                        img2, self.frame2 = self.vid2.read()
                    else:
                        self.frame1 = cv2.imread("./img/road.jfif")
                        self.frame2  = cv2.imread("./img/patient.jfif")
                    self.frame1 = imutils.resize(self.frame1,width=380)
                    self.frame2 = imutils.resize(self.frame2,width=380)
                    a = pickle.dumps(self.frame1)
                    b = pickle.dumps(self.frame2)
                    message = struct.pack("2Q",1000,len(a))+a
                    self.client_socket.sendall(message)
                    message = struct.pack("2Q",2000,len(b))+b
                    self.client_socket.sendall(message)
                    message = struct.pack("2Q",int(self.pos[0]),int(self.pos[1]))
                    self.client_socket.sendall(message)
                    message = struct.pack("2Q",3000,int(self.if_human))
                    # print(int(self.if_human))
                    self.client_socket.sendall(message)
                    # cv2.imshow(f"TO: {self.host_ip}2",self.frame2)
                    # cv2.imshow(f"TO: {self.host_ip}1",self.frame1)
                    if cv2.waitKey(1) == ord(" "):
                        self.connecting = False
                        self.Disconnect = True
                        break
                # if self.client_socket:
                #     self.client_socket.close()
            except Exception as e:
                print(e)
                print('[VIDEO FINISHED!]')
                self.connecting = False
                self.Disconnect = True
                # if self.client_socket:
                #     self.client_socket.close()

    def humanDetect(self):
        while self.connecting:
            # if self.if_video:
            #     img, self.frame1 = self.vid1.read()
            #     # img2, self.frame2 = self.vid2.read()
            # else:
            #     self.frame1 = cv2.imread("./img/road.jfif")
            #     # self.frame2  = cv2.imread("./img/patient.jfif")
            self.bbox, classs, confs, findPerson, frame1 = self.yolo.getDefaultOut(self.frame1)
            frame1 = cv2.resize(frame1,(360,240))
            if findPerson:
                self.if_human = True
                self.yolo.warning()
            else:
                self.if_human = False
                self.yolo.safe()
            # cv2.imshow("hdingj86",frame1)
            # if cv2.waitKey(1) & 0xff == ord('q'):
            #     cv2.destroyAllWindows()

    def Arduino_send(self, ard, data):
        while True:
            try:
                data = str(data)
                ard.write(data.encode())
                print(f"[SEND ARDUINO]{data}")
                break
            except:
                print("[SEND ERROR!]")
                break


    def Bed_Transport(self):
        print(self.pos)
        if self.pos == (17,5):
            self.Arduino_send(self.arduino, "@")
            self.pos = (5,12)
        elif self.pos == (5,12):
            self.Arduino_send(self.arduino, "$")
            self.pos = (17,5)
        self.transporting = False
        print(self.pos)








