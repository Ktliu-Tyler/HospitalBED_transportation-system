import tkinter as tk
from webExcel import webExcel
import time
import uiTool
import tool
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import threading


class PatientRecord:
    def __init__(self, window, Id, sheet):
        self.Id = Id
        self.titleList = ["姓名", "身分證字號", "性別", "生日", "年齡", "身高", "體重", "地址", "病患聯絡電話", "家屬聯絡電話", "病史"]
        self.sheet = sheet
        self.eWindow = ''
        self.database = r"./patientImg"
        self.edit_btt_img = tk.PhotoImage(file='./img/edit.png')
        self.originWindow = window
        self.rWindow = tk.Toplevel(window, bg='white')
        self.rWindow.title('Patient Record')
        self.rWindow.geometry('550x700')
        self.rWindow.resizable(0, 0)
        self.rWindow.iconbitmap('./RImg/icon.ico')
        self.fontStyle = ('Microsoft Yahei', 12)
        self.rWindowSetting()

    def rWindowSetting(self):
        self.load_img()
        self.variableDeclare()
        self.titleDeclare()
        self.getRecordValue()
        self.entryDeclare()
        self.functionObjectDeclare()

    def load_img(self):
        self.imageList = []
        self.name_img = tk.PhotoImage(file='./RImg/name.png')
        self.imageList.append(self.name_img)
        self.ID_img = tk.PhotoImage(file='./RImg/ID.png')
        self.imageList.append(self.ID_img)
        self.gender_img = tk.PhotoImage(file='./RImg/gender.png')
        self.imageList.append(self.gender_img)
        self.birth_img = tk.PhotoImage(file='./RImg/birth.png')
        self.imageList.append(self.birth_img)
        self.age_img = tk.PhotoImage(file='./RImg/age.png')
        self.imageList.append(self.age_img)
        self.height_img = tk.PhotoImage(file='./RImg/height.png')
        self.imageList.append(self.height_img)
        self.weight_img = tk.PhotoImage(file='./RImg/weight.png')
        self.imageList.append(self.weight_img)
        self.address_img = tk.PhotoImage(file='./RImg/address.png')
        self.imageList.append(self.address_img)
        self.phone_img = tk.PhotoImage(file='./RImg/phone.png')
        self.imageList.append(self.phone_img)
        self.emergency_img = tk.PhotoImage(file='./RImg/emergency.png')
        self.imageList.append(self.emergency_img)
        self.record_img = tk.PhotoImage(file='./RImg/record.png')
        self.imageList.append(self.record_img)
        self.patient_img = tk.PhotoImage(file='./RImg/patient.png')
        self.imageList.append(self.patient_img)
        self.title_img = tk.PhotoImage(file='./RImg/title.png')
        self.imageList.append(self.title_img)
        self.title2_img = tk.PhotoImage(file='./RImg/title2.png')
        self.imageList.append(self.title2_img)

    def titleDeclare(self):
        self.recordTitle = tk.Label(self.rWindow, bg='white')
        self.recordTitle.configure(image=self.imageList[12])
        self.recordTitle.grid(row=0, column=0, columnspan=4)
        self.nameTitle = tk.Label(self.rWindow, bg='white')
        self.nameTitle.configure(image=self.imageList[0])
        self.nameTitle.grid(row=1, column=0)
        self.IDTitle = tk.Label(self.rWindow, bg='white')
        self.IDTitle.configure(image=self.imageList[1])
        self.IDTitle.grid(row=2, column=0)
        self.genderTitle = tk.Label(self.rWindow, bg='white')
        self.genderTitle.configure(image=self.imageList[2])
        self.genderTitle.grid(row=3, column=0)
        self.birthTitle = tk.Label(self.rWindow, bg='white')
        self.birthTitle.configure(image=self.imageList[3])
        self.birthTitle.grid(row=4, column=0)
        self.ageTitle = tk.Label(self.rWindow, bg='white')
        self.ageTitle.configure(image=self.imageList[4])
        self.ageTitle.grid(row=5, column=0)
        self.heightTitle = tk.Label(self.rWindow, bg='white')
        self.heightTitle.configure(image=self.imageList[5])
        self.heightTitle.grid(row=6, column=0)
        self.weightTitle = tk.Label(self.rWindow, bg='white')
        self.weightTitle.configure(image=self.imageList[6])
        self.weightTitle.grid(row=7, column=0)
        self.addressTitle = tk.Label(self.rWindow, bg='white')
        self.addressTitle.configure(image=self.imageList[7])
        self.addressTitle.grid(row=8, column=0)
        self.phoneTitle = tk.Label(self.rWindow, bg='white')
        self.phoneTitle.configure(image=self.imageList[8])
        self.phoneTitle.grid(row=9, column=0)
        self.emergentTitle = tk.Label(self.rWindow, bg='white')
        self.emergentTitle.configure(image=self.imageList[9])
        self.emergentTitle.grid(row=10, column=0)
        self.patientPhoto = tk.Button(self.rWindow, bg='white', state=self.modify.get(), command=self.openFile)
        self.patientPhoto.configure(image=self.imageList[11])
        self.patientPhoto.grid(row=1, column=2, rowspan=3)
        self.recordTitle = tk.Label(self.rWindow, bg='white')
        self.recordTitle.configure(image=self.imageList[10])
        self.recordTitle.grid(row=4, column=2)

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
        self.emergent = tk.StringVar()
        self.record = tk.StringVar()
        self.modify = tk.StringVar()
        self.modify.set("disabled")
        self.variableList = []
        self.variableList.append(self.name)
        self.variableList.append(self.gender)
        self.variableList.append(self.birth)
        self.variableList.append(self.age)
        self.variableList.append(self.weight)
        self.variableList.append(self.height)
        self.variableList.append(self.ID)
        self.variableList.append(self.address)
        self.variableList.append(self.phone)
        self.variableList.append(self.emergent)
        self.variableList.append(self.record)

    def entryDeclare(self):
        self.nameEntry = tk.Entry(self.rWindow, textvariable=self.variableList[0], state=self.modify.get(), font=self.fontStyle)
        self.nameEntry.grid(row=1, column=1)
        self.IDEntry = tk.Entry(self.rWindow, textvariable=self.variableList[6], state=self.modify.get(), font=self.fontStyle)
        self.IDEntry.grid(row=2, column=1)
        self.genderEntry = tk.Entry(self.rWindow, textvariable=self.variableList[1], state=self.modify.get(), font=self.fontStyle)
        self.genderEntry.grid(row=3, column=1)
        self.birthEntry = tk.Entry(self.rWindow, textvariable=self.variableList[2], state=self.modify.get(), font=self.fontStyle)
        self.birthEntry.grid(row=4, column=1)
        self.ageEntry = tk.Entry(self.rWindow, textvariable=self.variableList[3], state=self.modify.get(), font=self.fontStyle)
        self.ageEntry.grid(row=5, column=1)
        self.heightEntry = tk.Entry(self.rWindow, textvariable=self.variableList[5], state=self.modify.get(), font=self.fontStyle)
        self.heightEntry.grid(row=6, column=1)
        self.weightEntry = tk.Entry(self.rWindow, textvariable=self.variableList[4], state=self.modify.get(), font=self.fontStyle)
        self.weightEntry.grid(row=7, column=1)
        self.addressEntry = tk.Entry(self.rWindow, textvariable=self.variableList[7], state=self.modify.get(), font=self.fontStyle)
        self.addressEntry.grid(row=8, column=1)
        self.phoneEntry = tk.Entry(self.rWindow, textvariable=self.variableList[8], state=self.modify.get(), font=self.fontStyle)
        self.phoneEntry.grid(row=9, column=1)
        self.emergentEntry = tk.Entry(self.rWindow, textvariable=self.variableList[9], state=self.modify.get(), font=self.fontStyle)
        self.emergentEntry.grid(row=10, column=1)
        self.recordEntry = tk.Text(self.rWindow, height='15', width='30')
        self.recordEntry.insert(1.0, self.variableList[10].get())
        self.recordEntry.configure(state=self.modify.get())
        self.recordEntry.grid(row=5, column=2, rowspan=4)
        self.object = [
            self.nameEntry, self.IDEntry, self.genderEntry, self.birthEntry, self.ageEntry, self.heightEntry, self.weightEntry,
            self.addressEntry, self.phoneEntry, self.emergentEntry, self.recordEntry, self.patientPhoto
        ]

    def functionObjectDeclare(self):
        self.eButton = tk.Button(self.rWindow, bg='white', relief=tk.FLAT, image=self.edit_btt_img,
                                 command=self.changeState).grid(row=9, column=2, rowspan=1)
        self.cButton = tk.Button(self.rWindow, bg='white', relief=tk.FLAT, image=self.edit_btt_img,
                                 command=self.cancel).grid(row=10, column=2, rowspan=1)

    def cancel(self):
        if self.modify.get() == "normal":
            self.notSaveExcel()
            self.modify.set("disabled")
            for obj in self.object:
                obj.configure(state=self.modify.get())


    def changeState(self):
        if self.modify.get() == "disabled":
            self.modify.set("normal")
            for obj in self.object:
                obj.configure(state=self.modify.get())
        elif self.modify.get() == "normal":
            self.saveExcel()
            self.modify.set("disabled")
            for obj in self.object:
                obj.configure(state=self.modify.get())

    def notSaveExcel(self):
        data = self.data
        self.name.set(data[2])
        self.ID.set(data[8])
        self.gender.set(data[3])
        self.birth.set(data[4])
        self.age.set(data[5] + " 歲")
        self.height.set(data[7] + " 公分")
        self.weight.set(data[6] + " 公斤")
        self.address.set(data[9])
        self.phone.set("0" + data[10])
        self.emergent.set("0" + data[11])
        self.record.set(data[12])
        self.recordEntry.delete(1.0, "end")
        self.recordEntry.insert(1.0, data[12])
        self.patientPhoto.configure(image=self.patient_img)
        self.patientPhoto.grid(row=1, column=2, rowspan=3)

    def openFile(self):
        filetypes = (
            ('img files', '*.png'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )
        self.patient_img_path = filename

        # showinfo(
        #     title='Selected File',
        #     message=filename
        # )
        try:
            photo = self.sheet.imgMaster.readImageFromSaveFile('', self.patient_img_path)
            self.patient_img_temp = tool.process_patient_image(photo)
            self.patientPhoto.configure(image=self.patient_img_temp)
            self.patientPhoto.grid(row=1, column=2, rowspan=3)
        except:
            pass

    def saveExcel(self):
        self.patient_img = self.patient_img_temp
        index, find = self.sheet.findSheetValue("patientCreditId", str(self.variableList[6].get()))
        wlen = len(str(self.variableList[4].get()))
        hlen = len(str(self.variableList[5].get()))
        self.variableList[10].set(str(self.recordEntry.get(1.0, "end")).rstrip("\n"))
        print(self.variableList[10].get())
        patientImgUrl = self.sheet.imgMaster.uploadImageFromFile(self.patient_img_path).link
        try:
            os.remove(os.path.join(self.database, f"{self.variableList[6].get()}.png"))
        except:
            print("[LOAD ERROR] You have no access to delete image!")
        self.sheet.imgMaster.getImageFromUrl(patientImgUrl, self.database, f"{self.variableList[6].get()}.png")
        if find:
            self.sheet.updateSpecificSheetData(
                index,
                patientName=str(self.variableList[0].get()), patientGender=str(self.variableList[1].get()),
                patientBirth=str(self.variableList[2].get()), patientWeight=str(self.variableList[4].get())[:wlen - 3],
                patientHeight=str(self.variableList[5].get())[:hlen - 3],
                patientCreditId=str(self.variableList[6].get()),
                patientAddressPlace=str(self.variableList[7].get()),
                patientPhoneNum=str(self.variableList[8].get())[1:],
                patientEmergencyContactPhoneNum=str(self.variableList[9].get())[1:],
                patientIllness=str(self.variableList[10].get())
            )
            self.sheet.uploadPatientPhotoUrl(index, patientImgUrl)
        else:
            self.sheet.sendPatientData(
                patientName=str(self.variableList[0].get()), patientGender=str(self.variableList[1].get()),
                patientBirth=str(self.variableList[2].get()), patientWeight=str(self.variableList[4].get())[:wlen - 3],
                patientHeight=str(self.variableList[5].get())[:hlen - 3],
                patientCreditId=str(self.variableList[6].get()),
                patientAddressPlace=str(self.variableList[7].get()),
                patientPhoneNum=str(self.variableList[8].get())[1:],
                patientEmergencyContactPhoneNum=str(self.variableList[9].get())[1:],
                patientIllness=str(self.variableList[10].get())
            )
            newId = self.sheet.getNewId()
            self.sheet.uploadPatientPhotoUrl(newId, patientImgUrl)

    def getRecordValue(self):
        self.index, _ = self.sheet.findSheetValue("patientCreditId", self.Id)
        self.data = self.sheet.getRowSheetData(self.index, verbose=True)
        data = self.data
        self.name.set(data[2])
        self.ID.set(data[8])
        self.gender.set(data[3])
        self.birth.set(data[4])
        self.age.set(data[5] + " 歲")
        self.height.set(data[7] + " 公分")
        self.weight.set(data[6] + " 公斤")
        self.address.set(data[9])
        self.phone.set("0" + data[10])
        self.emergent.set("0" + data[11])
        self.record.set(data[12])
        try:
            photoURL = data[14]
            print(photoURL)
        except:
            photoURL = "https://i.imgur.com/LwUGjC0.png"
        if not os.path.exists(self.database):
            os.mkdir(self.database)
        self.sheet.imgMaster.getImageFromUrl(photoURL, self.database, f"{data[8]}.png")
        photo = self.sheet.imgMaster.readImageFromSaveFile(self.database, f"{data[8]}.png")
        self.patient_img = tool.process_patient_image(photo)
        self.patient_img_temp = self.patient_img
        self.patient_img_path = os.path.join(self.database, f"{data[8]}.png")
        self.patientPhoto.configure(image=self.patient_img)
        self.patientPhoto.grid(row=1, column=2, rowspan=3)
        self.variableList.append(self.name)
        self.variableList.append(self.gender)
        self.variableList.append(self.birth)
        self.variableList.append(self.age)
        self.variableList.append(self.weight)
        self.variableList.append(self.height)
        self.variableList.append(self.ID)
        self.variableList.append(self.address)
        self.variableList.append(self.phone)
        self.variableList.append(self.emergent)
        self.variableList.append(self.record)


class QRcodeOption:
    def __init__(self, window, sheet, QRscan, QRidVar):
        self.window = window
        self.sheet = sheet
        self.QRsccan = QRscan
        self.name = "等待取得身分"
        self.QRidVar = QRidVar
        self.id = ""
        self.oWindow = tk.Toplevel(window, bg='white')
        self.oWindow.title('ID Get Choice')
        self.oWindow.geometry('210x300')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.oWindowSetting()

    def oWindowSetting(self):
        self.idVariable = tk.StringVar()
        self.idVariable.set(self.id)
        self.nameVariable = tk.StringVar()
        self.nameVariable.set(self.name)
        self.allOption()

    def allOption(self):
        self.titleLabel = tk.Label(self.oWindow, text="病例查詢選擇", font=self.fontStyle, bg="skyblue")
        self.titleLabel.grid(row=0, column=0, pady=5, padx=10)
        self.idLabel = tk.Label(self.oWindow, textvariable=self.nameVariable, font=self.fontStyle, bg="white")
        self.idLabel.grid(row=1, column=0, pady=2, padx=10)
        self.QRButton = tk.Button(self.oWindow, text="使用QR code", font=self.fontStyle, bg="white",
                                  command=self.QRcodeGetId)
        self.QRButton.grid(row=2, column=0, pady=2, padx=10)
        self.entryButton = tk.Button(self.oWindow, text="使用身分輸入", font=self.fontStyle, bg="white",
                                     command=self.EntryGetId)
        self.entryButton.grid(row=3, column=0, pady=2, padx=10)
        self.findButton = tk.Button(self.oWindow, text="確定", font=self.fontStyle, bg="white", command=self.findRecord)
        self.findButton.grid(row=4, column=0, pady=2, padx=10)

    def QRcodeGetId(self):
        self.QRScanWindow = QRcodeScan(self.oWindow, self.sheet, self.nameVariable, self.idVariable, self.QRsccan,
                                       self.QRidVar)

    def EntryGetId(self):
        self.entryWindow = IdEntry(self.oWindow, self.sheet, self.nameVariable, self.idVariable)

    def findRecord(self):
        if len(str(self.idVariable.get())) > 9:
            createRecordWindow(self.window, str(self.idVariable.get()), self.sheet)
        else:
            uiTool.createMessageBox("[ID ERROR]", "You haven't get a credit!")


class QRcodeScan:
    def __init__(self, window, sheet, nameVariable, idVariable, QRscan, QRid):
        self.QRscan = QRscan
        self.oWindow = window
        self.sheet = sheet
        self.idVar = idVariable
        self.QRid = QRid
        self.nameVar = nameVariable
        self.QRWindow = tk.Toplevel(window, bg='white')
        self.QRWindow.title('QRcode Scan')
        self.QRWindow.geometry('190x170')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.optionBlock()

    def optionBlock(self):
        self.idLabel = tk.Label(self.QRWindow, textvariable=self.nameVar, font=self.fontStyle, bg="skyblue",
                                anchor="center")
        self.idLabel.grid(row=0, column=0, pady=2, padx=10)
        self.idLabel = tk.Label(self.QRWindow, textvariable=self.idVar, font=self.fontStyle, bg="white",
                                anchor="center")
        self.idLabel.grid(row=1, column=0, pady=2, padx=10)
        self.cButton = tk.Button(self.QRWindow, text="開始掃描", font=self.fontStyle, bg="white", command=self.scaning,
                                 anchor="center")
        self.cButton.grid(row=2, column=0, pady=2, padx=10)

    def scaning(self):
        self.QRscan.set(True)
        time.sleep(1)
        if self.QRid.get() != "":
            print(self.QRid.get())
            index, find = self.sheet.findSheetValue("patientCreditId", str(self.QRid.get()))
            if find:
                data = self.sheet.getRowSheetData(index)
                self.nameVar.set(data[2])
                self.idVar.set(self.QRid.get())
            else:
                self.nameVar.set("等待取得身分")
                self.idVar.set("")
                uiTool.createMessageBox("[SCAN ERROR]", "Please scan again!")
            self.QRscan.set(False)


class IdEntry:
    def __init__(self, window, sheet, nameVarible, idVariable):
        self.oWindow = window
        self.sheet = sheet
        self.nameVar = nameVarible
        self.idVar = idVariable
        self.enWindow = tk.Toplevel(window, bg='white')
        self.enWindow.title('ID Entry')
        self.enWindow.geometry('350x160')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.optionSetting()

    def optionSetting(self):
        self.idLabel = tk.Label(self.enWindow, textvariable=self.nameVar, font=self.fontStyle, bg="skyblue")
        self.idLabel.grid(row=0, column=0, pady=2, padx=10)
        self.IDEntry = tk.Entry(self.enWindow, textvariable=self.idVar, font=self.fontStyle, bg="white")
        self.IDEntry.grid(row=1, column=0, pady=2, padx=10)
        self.cButton = tk.Button(self.enWindow, text="確定", font=self.fontStyle, bg="white", command=self.checkID)
        self.cButton.grid(row=2, column=0, pady=2, padx=10)

    def checkID(self):
        index, find = self.sheet.findSheetValue("patientCreditId", str(self.idVar.get()))
        if find:
            data = self.sheet.getRowSheetData(index)
            self.nameVar.set(data[2])
        else:
            self.nameVar.set("等待取得身分")
            self.idVar.set("")
            uiTool.createMessageBox("[ID ERROR]", "Please check your id!")


def createRecordWindow(window, id, sheet):
    record = PatientRecord(window, id, sheet)


def createQRWindow(window, sheet, QRscan, QRid):
    QRwindow = QRcodeOption(window, sheet, QRscan, QRid)


if __name__ == "__main__":
    window = tk.Tk()
    window.title('main')
    window.geometry('200x200')
    QRscan = tk.BooleanVar()
    QRid = tk.StringVar()
    sheet = webExcel.Sheet()
    buttonRe = tk.Button(window, text='閉嘴啦', command=lambda: createRecordWindow(window, "A000000000", sheet))
    buttonRe.pack()
    buttonQR = tk.Button(window, text='zp4', command=lambda: createQRWindow(window, sheet, QRscan, QRid))
    buttonQR.pack()
    window.mainloop()
