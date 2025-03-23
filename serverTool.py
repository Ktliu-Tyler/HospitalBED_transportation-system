import socket, pickle, struct
import threading
import astarTool as Astar
import newUIRecordToolBeautify as UIRecordTool
import uiTool
import tool
from webExcel.webExcel import Sheet
import QRCodeModule


RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"
WHITE = "white"
BLACK = "black"
PURPLE = "purple"
ORANGE = "orange"
GREY = "gray"
TURQUOISE = "turquoise"


class Server:
    def __init__(self, port):
        self.port = port
        self.bedCount = 1
        self.bedNum = 0
        self.if_human = 0
        self.bedList = []
        self.allThread = []
        self.path = []
        self.QRimg = None
        self.Id = None
        self.S = None
        self.E = None
        self.wifiSet = False
        self.close = False
        self.notFinish = True
        self.moving = False
        self.close = False
        self.if_connect = False
        self.is_starting = False
        self.QRModule = QRCodeModule.QRCodeScanner(innerCapture=False)
        self.window = uiTool.UI()
        self.window.QRscan.set(False)
        self.window.QRid.set("")
        self.settingALL()
        self.window.running()

    def settingALL(self):
        self.btnSetting()
        # 地圖設置
        Astar.draw(self.window.map_canvas, self.window.grid, Astar.WIDTH)
        self.astar = Astar.Brain(self.S, self.E, self.path)
        self.videoStream()
        self.window.window.after(200, self.update)

    def btnSetting(self):
        self.window.connect_btt.configure(command=self.starting)
        self.window.record_btt.configure(command=self.searchRecord)
        self.window.map_reset.configure(command=self.mapreset)
        self.window.map_btt.configure(command=self.Start)
        self.window.opt1.bind('<<ComboboxSelected>>', self.cbb_select)
        self.window.map_canvas.bind("<Button-1>", self.click_mouse_status)

    def searchRecord(self):
        t = threading.Thread(target=self.createQRwindow)
        t.daemon = True
        t.start()
        # if self.bedNum != 0:
        #     self.record = UIRecordTool.PatientRecord(self.window.window, self.idList[self.bedNum-1])

    def createQRwindow(self):
        try:
            self.sheet = Sheet()
            self.QRwindow = UIRecordTool.QRcodeOption(self.window.window, self.sheet, self.window.QRscan, self.window.QRid)
        except:
            uiTool.createMessageBox("[WIFI ERROR]", "You don't have a wifi connect!, please try again!")
            print("[Wifi ERROR] You don't connect Wifi!")

    def wifiSetting(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        print('[HOST IP]:', self.host_ip)
        self.s_address = (self.host_ip, self.port)
        self.s.bind(self.s_address)
        self.s.listen(5)
        print("[Listening]window at", self.s_address)

    def wifiConnecting(self):# 啟動連線
        if not self.close:
            if not self.wifiSet:
                self.wifiSetting()
                self.wifiSet = True
            self.c, self.addr = self.s.accept()
            b = tool.Bed(self.c, self.addr, f"Bed{self.bedCount}")
            self.window.Connect_List.append(b.name)
            self.bedList.append(b)
            self.window.opt1['values'] = self.window.Connect_List
            self.recving()
            self.bedCount += 1
            self.bedNum += 1
            self.window.lab1str.set(str(f'可用病床數量: {self.bedNum}輛'))
            print('[CLIENT {} CONNECTED!]'.format(self.addr))
            print("[TOTAL CLIENTS ",threading.activeCount() - 2,"]")
        else:
            return
        return

    def Start(self):#演算開始
        if self.S != None and self.E != None and not(self.astar.Start) and self.notFinish:
            print("[FIND PATH]")
            self.notFinish = False
            self.is_starting = False
            self.moving = True
            for row in self.window.grid:
                for spot in row:
                    spot.update_neighbors(self.window.grid)
            self.window.map_btt.configure(image=self.window.btt_img_send)
            t = threading.Thread(target=self.astar.algorithm,args=(lambda: Astar.draw(self.window.map_canvas, self.window.grid, self.window.WIDTH), self.window.grid, self.S, self.E))
            t.daemon = True
            self.allThread.append(t)
            t.start()
        else:
            if not(self.astar.Start) and not(self.notFinish):
                print("[Send_PATH!]")
                self.sendData()
                self.notFinish = True
                self.moving = True

    def mapreset(self):#刷新地圖
        if not(self.astar.Start):
            print("[CLEAR MAP]")
            self.S = None
            self.E = None
            self.window.grid = Astar.make_grid(Astar.ROW, Astar.COL, Astar.WIDTH)
            self.window.map_canvas.create_image(0,0,anchor='nw',image=self.window.map)
            # self.map_canvas.grid(column=1, row=0, rowspan=2, padx=10, pady=10)
            self.notFinish = True

    def cbb_select(self, event): # 下拉式選單刷新
        if self.window.opt1.get() != "選擇裝置":
            name = self.window.opt1.get()
            count = int(name[3:len(name)])-1
            if self.window.opt1.get() == self.bedList[count].name and self.bedList[count].is_complete():
                if self.window.opt2.get() == '路徑鏡頭' :
                    self.window.Vimage = self.bedList[count].route_img
                    # print("route")
                elif self.window.opt2.get() == '病患鏡頭' :
                    self.window.Vimage = self.bedList[count].patient_img
                    # print("patient")
        elif self.window.opt1.get() == "選擇裝置":
                self.window.Vimage = self.window.Timage

        if not(self.astar.Start):
            self.window.map_canvas.create_image(0, 0, anchor='nw', image=self.window.map)
            # self.map_canvas.grid(column=1, row=0, rowspan=2, padx=10, pady=10)
            if self.S != None:
                self.S.draw(self.window.map_canvas)
            if self.E != None:
                self.E.draw(self.window.map_canvas)

    def click_mouse_status(self, event): # 地圖滑鼠點擊事件
        # print(event.x,event.y)
        for row in self.window.grid:
            for spot in row:
                if ((event.y > spot.y) and (event.y < spot.y + spot.width)) and ((event.x > spot.x) and (event.x < spot.x + spot.width)):
                    if not(spot.is_barrier()):
                        if self.E == None:
                            print(f"[DESTINATION]:({spot.col},{spot.row})")
                            spot.make_end()
                            self.E = spot
                            self.E.draw(self.window.map_canvas)

    def sendData(self): # 傳送訊息
        name = self.window.opt1.get()
        if name != "選擇裝置":
            count = int(name[3:len(name)])-1
            # print(count)
            path_bool = self.astar.path_if_dot
            path_dir = self.astar.path_dot_dir
            path_pos = self.astar.path_pos
            path_n_dir = []
            for i in path_dir:
                if i == "left":
                    path_n_dir.append(0)
                elif i == "up":
                    path_n_dir.append(1)
                elif i == "right":
                    path_n_dir.append(2)
                elif i == "down":
                    path_n_dir.append(3)
            for i in range(len(path_bool)):
                path_bool[i] = int(path_bool[i])
            client = self.bedList[count].client
            if client:
                try:
                    a = pickle.dumps(path_bool)
                    b = pickle.dumps(path_n_dir)
                    c = pickle.dumps(path_pos)
                    message = struct.pack("3Q",len(a),len(b),len(c))+a+b+c
                    client.sendall(message)
                except Exception as e:
                    print(e)
                    print('[Send Error!]')

    def ScaningQRcode(self, count):
        t = threading.Thread(target=self.ScanQRcode)
        t.daemon = True
        self.allThread.append(t)
        t.start()
        return

    def ScanQRcode(self):
        print("[QRCODE READY]")
        while True:
            if self.window.QRscan.get():
                print("[QRcode SCANING]")
                frame = self.QRimg
                myData, frame = self.QRModule.decodeQRCode(frame)
                if not(myData == ''):
                    print("[SCAN SUCCESS!]")
                    self.window.QRid.set(myData)
                    break

            if not self.c:
                print("[QRCODE DISCONNECT]")
                break

    def recvData(self): # 接收訊息
        count = self.bedCount-1
        print(self.bedCount)
        # print(count)
        try:
            if self.c: # if a client socket exists
                data1 = b""
                payload_size = struct.calcsize("2Q")
                self.ScaningQRcode(count)
                while not self.close:
                    while len(data1) < payload_size:
                        packet = self.bedList[count].client.recv(4*1024)
                        if not packet: break
                        data1 += packet
                    packed_msg_size1 = data1[:payload_size]
                    data1 = data1[payload_size:]
                    lab = struct.unpack("2Q", packed_msg_size1)[0]
                    msg_size1 = struct.unpack("2Q", packed_msg_size1)[1]
                    if lab == 1000 or lab == 2000:
                        while len(data1) < msg_size1:
                            data1 += self.bedList[count].client.recv(4*1024)
                        datas = data1
                        frame_data = data1[:msg_size1]
                        data1 = data1[msg_size1:]
                        frame = pickle.loads(frame_data)
                        if lab == 1000:
                            self.bedList[count].get_Rimg(frame)
                        elif lab == 2000:
                            self.QRimg = frame
                            self.bedList[count].get_Pimg(frame)
                    elif lab == 3000:
                        self.if_human = int(msg_size1)
                    else:
                        pos = (int(struct.unpack("2Q", packed_msg_size1)[1]),int(struct.unpack("2Q", packed_msg_size1)[0]))
                        self.bedList[count].get_pos(pos)
                        for row in self.window.grid:
                            for spot in row:
                                if spot.col == int(pos[0]) and spot.row == int(pos[1]) and self.notFinish:
                                    if self.window.opt1.get() == self.bedList[count].name:
                                        spot.make_start()
                                        if self.S != None :
                                            if (self.S.row,self.S.col) != pos:
                                                self.S.reset()
                                        self.S = spot
                                        self.S.draw(self.window.map_canvas)
                                        break
                                    elif self.window.opt1.get() == "選擇裝置":
                                        if self.S != None and self.notFinish:
                                            # print("pass3")
                                            self.window.map_canvas.create_image(0,0,anchor='nw',image=self.window.map)
                                            self.S.reset()
                                            self.S.delete(self.window.map_canvas)
                                            self.S = spot


                    if self.window.opt1.get() == self.bedList[count].name and self.bedList[count].is_complete():
                        if self.window.opt2.get() == '路徑鏡頭':
                            self.window.Vimage = self.bedList[count].route_img
                            # print("route")
                        elif self.window.opt2.get() == '病患鏡頭':
                            self.window.Vimage = self.bedList[count].patient_img
                            # print("patient")
                    elif self.window.opt1.get() == "選擇裝置":
                        self.window.Vimage = self.window.Timage
                        # print(self.bedList[count].name, self.bedList[count].is_complete())
            print(f"CLINET {self.bedList[count].name}({self.bedList[count].addr}) DISCONNECTED")
            if self.window.opt1.get() == self.bedList[count].name:
                self.window.opt1.current(0)
                self.window.Vimage = self.window.Timage
                if self.S != None and self.notFinish:
                    # print("pass3")
                    self.window.map_canvas.create_image(0,0,anchor='nw',image=self.window.map)
                    self.S.reset()
                    self.S.delete(self.window.map_canvas)

            self.window.Connect_List.remove(self.bedList[count].name)
            self.window.opt1['values'] = self.window.Connect_List
            self.window.map_reset()
            self.window.map_canvas.create_image(0,0,anchor='nw',image=self.window.map)
            self.bedNum -= 1
            self.window.lab1str.set(str(f'可用病床數量: {self.bedNum}輛'))
            if self.bedList[count]:
                self.bedList[count].client.close()

        except Exception as e:
            print(f"[CLINET DISCONNECTED]{self.bedList[count].name}({self.bedList[count].addr})")
            print(e)
            if self.window.opt1.get() == self.bedList[count].name:
                self.window.opt1.current(0)
                self.window.Vimage = self.window.window.Timage
            self.window.Connect_List.remove(self.bedList[count].name)
            self.window.opt1['values'] = self.window.Connect_List
            self.bedNum-=1
            self.window.lab1str.set(str(f'可用病床數量: {self.bedNum}輛'))
            if self.bedList[count]:
                self.bedList[count].client.close()

    def starting(self):#啟動連線線程
        t = threading.Thread(target=self.wifiConnecting)
        t.daemon = True
        self.allThread.append(t)
        t.start()
        return

    def sending(self):#啟動發訊線程
        t = threading.Thread(target=self.sendData)
        t.daemon = True
        self.allThread.append(t)
        t.start()
        return

    def recving(self):#啟動收訊線程
        t = threading.Thread(target=self.recvData)
        t.daemon = True
        self.allThread.append(t)
        t.start()
        return

    def videoStream(self):#影像串流
        self.Imgtk = tool.process_image(self.window.Vimage)
        self.window.video.imgtk = self.Imgtk
        self.window.video.configure(image=self.Imgtk)
        self.window.video.grid()
        self.window.video.after(10, self.videoStream)
        return

    def update(self):  # mainloop更新
        if self.notFinish:
            # self.map_canvas.create_image(0,0,anchor='nw',image=self.map)
            if self.S != None and self.E != None:
                if (self.S.col, self.S.row) == (self.E.col,self.E.row):
                    self.E = None
            elif self.E != None:
                self.E.draw(self.window.map_canvas)
            if self.S != None:
                self.S.draw(self.window.map_canvas)
            if self.S != None and self.E != None and self.notFinish:
                self.window.map_btt.configure(image=self.window.btt_img_calculate)
            else :
                self.window.map_btt.configure(image=self.window.btt_img_set)
        if self.if_human == 1:
            self.window.lab2str.set("有行人擋住路線")
        elif self.if_human == 0:
            self.window.lab2str.set("偵測無障礙物")
        elif self.if_human == 2:
            self.window.lab2str.set("有障礙物阻擋路線")
        self.window.window.after(200, self.update)
        return

