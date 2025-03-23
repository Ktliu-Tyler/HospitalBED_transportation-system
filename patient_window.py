from email.errors import ObsoleteHeaderDefect
import tkinter as tk
from tkinter import PhotoImage
import tkinter.messagebox
from cv2 import resizeWindow

class PatientRecord:
    def __init__(self, window):
        self.titleList = ["姓名", "身分證字號", "性別", "生日", "年齡", "身高", "體重", "地址", "病患聯絡電話", "家屬聯絡電話", "病史"]
        self.edit_btt_img = tk.PhotoImage(file='./img/edit.png')
        self.rWindow = tk.Toplevel(window, bg='white')
        self.rWindow.title('Patient Record')
        self.rWindow.geometry('500x700')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.rWindowSetting()

    def rWindowSetting(self):
        self.titleDeclare()
        self.variableDeclare()
        self.getRecordValue()
        self.labelDeclare()
        self.functionObjectDeclare()

    def titleDeclare(self):
        self.recordTitle = tk.Label(self.rWindow, bg='skyblue', text='~病患資料~', font=self.fontStyle).grid(row=0, column=1, rowspan=2)
        self.nameTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[0]}:", font=self.fontStyle).grid(row=2, column=0)
        self.IDTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[1]}:", font=self.fontStyle).grid(row=3, column=0)
        self.genderTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[2]}:", font=self.fontStyle).grid(row=4, column=0)
        self.birthTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[3]}:", font=self.fontStyle).grid(row=5, column=0)
        self.ageTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[4]}:", font=self.fontStyle).grid(row=6, column=0)
        self.heightTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[5]}:", font=self.fontStyle).grid(row=7, column=0)
        self.weightTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[6]}:", font=self.fontStyle).grid(row=8, column=0)
        self.addressTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[7]}:", font=self.fontStyle).grid(row=9, column=0)
        self.phoneTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[8]}:", font=self.fontStyle).grid(row=10, column=0)
        self.emergenTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[9]}:", font=self.fontStyle).grid(row=11, column=0)
        self.recordTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[10]}:", font=self.fontStyle).grid(row=12, column=0)

    def variableDeclare(self): 
        self.name = tk.StringVar()
        self.ID = tk.StringVar()
        self.gender = tk.StringVar()
        self.birth = tk.StringVar()
        self.age = tk.StringVar()
        self.height = tk.StringVar()
        self.weight = tk.StringVar()
        self.address = tk.StringVar()
        self.phone = tk.StringVar()
        self.emergen = tk.StringVar()
        self.record = tk.StringVar()

    def labelDeclare(self):
        self.nameLabel = tk.Label(self.rWindow, bg='white', textvariable=self.name, font=self.fontStyle).grid(row=2, column=1)
        self.IDLabel = tk.Label(self.rWindow, bg='white', textvariable=self.ID, font=self.fontStyle).grid(row=3, column=1)
        self.genderLabel = tk.Label(self.rWindow, bg='white', textvariable=self.gender, font=self.fontStyle).grid(row=4, column=1)
        self.birthLabel = tk.Label(self.rWindow, bg='white', textvariable=self.birth, font=self.fontStyle).grid(row=5, column=1)
        self.ageLabel = tk.Label(self.rWindow, bg='white', textvariable=self.age, font=self.fontStyle).grid(row=6, column=1)
        self.heightLabel = tk.Label(self.rWindow, bg='white', textvariable=self.height, font=self.fontStyle).grid(row=7, column=1)
        self.weightLabel = tk.Label(self.rWindow, bg='white', textvariable=self.weight, font=self.fontStyle).grid(row=8, column=1)
        self.addressLabel = tk.Label(self.rWindow, bg='white', textvariable=self.address, font=self.fontStyle).grid(row=9, column=1)
        self.phoneLabel = tk.Label(self.rWindow, bg='white', textvariable=self.phone, font=self.fontStyle).grid(row=10, column=1)
        self.emergenLabel = tk.Label(self.rWindow, bg='white', textvariable=self.emergen, font=self.fontStyle).grid(row=11, column=1)
        self.recordLabel = tk.Label(self.rWindow, bg='white', textvariable=self.record, font=self.fontStyle).grid(row=12, column=1, rowspan=2)
    
    def functionObjectDeclare(self):
        self.eButton = tk.Button(self.rWindow, image=self.edit_btt_img, command=self.createEditWindow).grid(row=13, column=1, rowspan=2)

    def getRecordValue(self):
        pass

    def createEditWindow(self):
        self.eWindow = EditPatientRecord(self.rWindow, self.titleList)



class EditPatientRecord:
    def __init__(self, window, titleList):
        self.titleList = titleList
        self.check_btt_img = tk.PhotoImage(file='./img/check.png')
        self.eWindow = tk.Toplevel(window, bg='white')
        self.eWindow.title('Edit Patient Record')
        self.eWindow.geometry('500x700')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.eWindowSetting()

    def eWindowSetting(self):
        self.labelDeclare()
        self.entryDeclare()
        self.functionObjectDeclare()

    def labelDeclare(self):
        self.recordTitle = tk.Label(self.eWindow, bg='skyblue', text='~修改資料~', font=self.fontStyle).grid(row=0, column=1, rowspan=2)
        self.nameLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[0]}:", font=self.fontStyle).grid(row=2, column=0)
        self.IDLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[1]}:", font=self.fontStyle).grid(row=3, column=0)
        self.genderLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[2]}:", font=self.fontStyle).grid(row=4, column=0)
        self.birthLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[3]}:", font=self.fontStyle).grid(row=5, column=0)
        self.ageLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[4]}:", font=self.fontStyle).grid(row=6, column=0)
        self.heightLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[5]}:", font=self.fontStyle).grid(row=7, column=0)
        self.weightLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[6]}:", font=self.fontStyle).grid(row=8, column=0)
        self.addressLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[7]}:", font=self.fontStyle).grid(row=9, column=0)
        self.phoneLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[8]}:", font=self.fontStyle).grid(row=10, column=0)
        self.emergenLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[9]}:", font=self.fontStyle).grid(row=11, column=0)
        self.recordLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[10]}:", font=self.fontStyle).grid(row=12, column=0, rowspan=2)

    def entryDeclare(self):   
        self.nameEntry = tk.Entry(self.eWindow).grid(row=2, column=1)
        self.IDEntry = tk.Entry(self.eWindow).grid(row=3, column=1)
        self.genderEntry = tk.Entry(self.eWindow).grid(row=4, column=1)
        self.birthEntry = tk.Entry(self.eWindow).grid(row=5, column=1)
        self.ageEntry = tk.Entry(self.eWindow).grid(row=6, column=1)
        self.heightEntry = tk.Entry(self.eWindow).grid(row=7, column=1)
        self.weightEntry = tk.Entry(self.eWindow).grid(row=8, column=1)
        self.addressEntry = tk.Entry(self.eWindow).grid(row=9, column=1)
        self.phoneEntry = tk.Entry(self.eWindow).grid(row=10, column=1)
        self.emergenEntry = tk.Entry(self.eWindow).grid(row=11, column=1)
        self.recordEntry = tk.Entry(self.eWindow).grid(row=12, column=1)

    def functionObjectDeclare(self):
        self.cButton = tk.Button(self.eWindow, bg='white', image=self.check_btt_img, command=self.saveExcel).grid(row=14, column=1, rowspan=2)

    def saveExcel(self):
        pass

def createWindow(window):
    record = PatientRecord(window)


if __name__=="__main__":
    window = tk.Tk()
    window.title('main')
    window.geometry('500x700')
    button = tk.Button(window, text = '爛', command=lambda: createWindow(window))
    button.pack()
    window.mainloop()


