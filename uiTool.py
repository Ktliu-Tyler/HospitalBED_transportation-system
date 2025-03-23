import cv2
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import astarTool as Astar
import tool

class UI:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 510
        self.ROW = 20
        self.COL = 17
        self.grid = Astar.make_grid(Astar.ROW, Astar.COL, Astar.WIDTH)
        self.IPbuf = str(f'可用病床數量: 0輛')
        self.cbuf = str('偵測無障礙物')
        self.Connect_List = ['選擇裝置']
        self.Camera_List = ['路徑鏡頭', '病患鏡頭']
        self.window = Tk()
        self.window.title("Automatic Hospital Bed Delivery System")
        self.window.resizable(0, 0)
        self.window.configure(bg='white')
        self.setting()

    def setting(self):
        self.imageDeclare()
        self.windowVariable()
        self.optionBlock()
        self.frameBlock()
        self.mapBlock()
        self.roadSet()

    def imageDeclare(self):
        # 圖片
        self.Timage = cv2.imread('./img/hospital.png')
        self.ip_img = PhotoImage(file='./img/iptext.png')
        self.connect_img = PhotoImage(file='./img/cnt_search.png')
        self.map = PhotoImage(file='./img/map.png')
        self.btt_img_short = PhotoImage(file='./img/button_small.png')
        self.btt_img_send = PhotoImage(file='./img/button_send.png')
        self.btt_img_set = PhotoImage(file='./img/button_set.png')
        self.btt_img_calculate = PhotoImage(file='./img/button_calculate.png')
        self.btt_img_clear = PhotoImage(file='./img/button_clear.png')
        self.btt_img_searching = PhotoImage(file="./img/button_searching.png")
        self.btt_img_long = PhotoImage(file='./img/button.png')
        self.record_img = PhotoImage(file='./img/record.png')

    def windowVariable(self):
        # 視窗變數
        self.Bttext = StringVar()
        self.Bttext.set("搜索裝置")
        self.lab1str = StringVar(value=self.IPbuf)
        self.lab2str = StringVar(value=self.cbuf)
        self.Vimage = self.Timage
        self.QRscan = BooleanVar()
        self.QRid = StringVar()

    def optionBlock(self):
        # 選擇區塊
        self.select_frm = Frame(self.window, bg="white", width=500, height=300, )
        self.select_frm.grid(column=0, row=0, padx=10, pady=10)
        self.connect_btt = Button(self.select_frm, bg='white', image=self.connect_img, width=100, height=50,
                                  borderwidth=0)
        self.connect_btt.configure(textvariable=self.Bttext)
        self.connect_btt.grid(column=0, row=1, padx=10, pady=10)
        self.record_btt = Button(self.select_frm, bg='white', image=self.record_img, width=100, height=50,
                                  borderwidth=0)
        self.record_btt.grid(column=0, row=2, padx=10, pady=10)
        self.opt1 = ttk.Combobox(self.select_frm, font=('Helvetica', 20))
        self.opt1['values'] = self.Connect_List
        self.opt1.current(0)
        self.opt1.grid(column=1, row=1, padx=10, pady=10)
        self.opt2 = ttk.Combobox(self.select_frm, font=('Helvetica', 20))
        self.opt2['values'] = self.Camera_List
        self.opt2.current(0)
        self.opt2.grid(column=1, row=2, padx=10, pady=10)
        self.ip_l = Label(self.select_frm, textvariable=self.lab1str, bg="#002060", fg="white", font=('Helvetica', 20),
                          width=28)
        self.ip_l.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

    def frameBlock(self):
        # 影像區塊
        self.video_frm = Frame(self.window, bg="#002060", width=500, height=300)
        self.video_frm.grid(column=0, row=1, rowspan=2, padx=10, pady=10)
        self.Imgtk = tool.process_image(self.Vimage)
        self.video = Label(self.video_frm, bg="gray")
        self.video.configure(image=self.Imgtk)
        self.video.grid(row=1, padx=3, pady=3)
        self.TrackLab = Label(self.video_frm)
        self.TrackLab.configure(width=22, bg="#002060", textvariable=self.lab2str, fg="white", font=('Helvetica', 20))
        self.TrackLab.grid(row=2, padx=3, pady=3)

    def mapBlock(self):
        # 地圖區塊
        self.map_canvas = Canvas(self.window, bg="green", width=600, height=504)
        self.map_canvas.configure(highlightthickness=0)
        self.map_canvas.create_image(0, 0, anchor='nw', image=self.map)
        self.map_canvas.grid(column=1, columnspan=2, row=0, rowspan=2, padx=10, pady=10)

    def roadSet(self):
        # 路徑規劃按鈕
        self.map_btt = Button(self.window, bg='white', image=self.btt_img_set, text="規劃路徑", width=300, height=48,
                              borderwidth=0)
        self.map_btt.grid(column=1, row=2, padx=10, pady=10)
        self.map_reset = Button(self.window, bg='white', image=self.btt_img_clear, text="規劃路徑", width=300, height=48,
                                borderwidth=0)
        self.map_reset.grid(column=2, row=2, padx=10, pady=10)

    def running(self):
        self.window.mainloop()
        self.window.quit()

def createMessageBox(title, message):
    messagebox.showinfo(title, message)


if __name__ == "__main__":
    window = UI()
    window.running()