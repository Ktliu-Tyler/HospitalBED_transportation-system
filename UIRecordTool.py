import time
import tkinter as tk
from webExcel import webExcel
import uiTool
import tool
import pickle

class PatientRecord:
    def __init__(self, window, Id, sheet):
        self.Id = Id
        self.titleList = ["姓名", "身分證字號", "性別", "生日", "年齡", "身高", "體重", "地址", "病患聯絡電話", "家屬聯絡電話", "病史"]
        self.sheet = sheet
        self.edit_btt_img = tk.PhotoImage(file='./img/edit.png')
        self.rWindow = tk.Toplevel(window, bg='white')
        self.rWindow.title('Patient Record')
        self.rWindow.geometry('700x700')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.rWindowSetting()

    def rWindowSetting(self):
        self.load_img()
        self.titleDeclare()
        self.variableDeclare()
        self.labelDeclare()
        self.getRecordValue()
        self.functionObjectDeclare()
        self.rWindow.mainloop()

    def load_img(self):
        self.imageList = []
        # self.name_img = tk.PhotoImage()
        # self.imageList.append(self.name_img)


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
        self.emergentTitle = tk.Label(self.rWindow, bg='white', text=f"{self.titleList[9]}:", font=self.fontStyle).grid(row=11, column=0)
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
        self.emergent = tk.StringVar()
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
        self.emergentLabel = tk.Label(self.rWindow, bg='white', textvariable=self.emergent, font=self.fontStyle).grid(row=11, column=1)
        self.recordLabel = tk.Label(self.rWindow, bg='white', textvariable=self.record, font=self.fontStyle).grid(row=12, column=1)
    
    def functionObjectDeclare(self):
        self.eButton = tk.Button(self.rWindow, image=self.edit_btt_img, command=self.createEditWindow).grid(row=13, column=1, rowspan=2)

    def getRecordValue(self):
        self.index, _ = self.sheet.findSheetValue("patientCreditId", self.Id)
        self.data = self.sheet.getRowSheetData(self.index)
        data = self.data
        self.dataOld = self.data
        self.name.set(data[2])
        self.ID.set(data[8])
        self.gender.set(data[3])
        self.birth.set(data[4])
        self.age.set(data[5]+" 歲")
        self.height.set(data[7]+" 公分")
        self.weight.set(data[6]+" 公斤")
        self.address.set(data[9])
        self.phone.set("0"+data[10])
        self.emergent.set("0"+data[11])
        self.record.set(data[12])
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

    def createEditWindow(self):
        self.eWindow = EditPatientRecord(self.rWindow, self.titleList, self.variableList, self.sheet, self.imageList)
        #x04
        # self.rWindow.update(200, )
        if self.eWindow.upload:
            self.variableList = self.eWindow.variableList


class EditPatientRecord:
    def __init__(self, window, titleList, variableList, sheet, imageList):
        self.upload = True
        self.close = False
        self.sheet = sheet
        self.imageList = imageList
        self.dataOld = []
        for v in variableList:
            self.dataOld.append(v.get())
        self.variableList = variableList
        self.titleList = titleList
        self.check_btt_img = tk.PhotoImage(file='./img/check.png')
        self.eWindow = tk.Toplevel(window, bg='white')
        self.eWindow.title('Edit Patient Record')
        self.eWindow.geometry('700x700')
        self.fontStyle = ('Microsoft Yahei', 20)
        self.eWindowSetting()

    def eWindowSetting(self):
        self.labelDeclare()
        self.entryDeclare()
        self.functionObjectDeclare()
        self.eWindow.protocol("WM_DELETE_WINDOW", self.notSaveExcel)
        self.eWindow.mainloop()

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
        self.emergentLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[9]}:", font=self.fontStyle).grid(row=11, column=0)
        self.recordLabel = tk.Label(self.eWindow, bg='white', text=f"{self.titleList[10]}:", font=self.fontStyle).grid(row=12, column=0, rowspan=2)

    def entryDeclare(self):
        self.nameEntry = tk.Entry(self.eWindow, textvariable=self.variableList[0], font=self.fontStyle).grid(row=2, column=1)
        self.IDEntry = tk.Entry(self.eWindow, textvariable=self.variableList[6], font=self.fontStyle).grid(row=3, column=1)
        self.genderEntry = tk.Entry(self.eWindow, textvariable=self.variableList[1], font=self.fontStyle).grid(row=4, column=1)
        self.birthEntry = tk.Entry(self.eWindow, textvariable=self.variableList[2], font=self.fontStyle).grid(row=5, column=1)
        self.ageEntry = tk.Entry(self.eWindow, textvariable=self.variableList[3], font=self.fontStyle).grid(row=6, column=1)
        self.heightEntry = tk.Entry(self.eWindow, textvariable=self.variableList[5], font=self.fontStyle).grid(row=7, column=1)
        self.weightEntry = tk.Entry(self.eWindow, textvariable=self.variableList[4], font=self.fontStyle).grid(row=8, column=1)
        self.addressEntry = tk.Entry(self.eWindow, textvariable=self.variableList[7], font=self.fontStyle).grid(row=9, column=1)
        self.phoneEntry = tk.Entry(self.eWindow, textvariable=self.variableList[8], font=self.fontStyle).grid(row=10, column=1)
        self.emergentEntry = tk.Entry(self.eWindow, textvariable=self.variableList[9], font=self.fontStyle).grid(row=11, column=1)
        self.recordEntry = tk.Entry(self.eWindow, textvariable=self.variableList[10], font=self.fontStyle).grid(row=12, column=1)

    def functionObjectDeclare(self):
        self.cButton = tk.Button(self.eWindow, bg='white', image=self.check_btt_img, command=self.saveExcel).grid(row=14, column=1, rowspan=2)

    def notSaveExcel(self):
        self.update = False
        for index, v in enumerate(self.variableList):
            v.set(self.dataOld[index])
        self.eWindow.destroy()
        del self

    def saveExcel(self):
        index, find = self.sheet.findSheetValue("patientCreditId", str(self.variableList[6].get()))
        wlen = len(str(self.variableList[4].get()))
        hlen = len(str(self.variableList[5].get()))
        if find:
            self.sheet.updateSpecificSheetData(
                index,
                patientName=str(self.variableList[0].get()), patientGender=str(self.variableList[1].get()),
                patientBirth=str(self.variableList[2].get()), patientWeight=str(self.variableList[4].get())[:wlen-3],
                patientHeight=str(self.variableList[5].get())[:hlen-3], patientCreditId=str(self.variableList[6].get()),
                patientAddressPlace=str(self.variableList[7].get()), patientPhoneNum=str(self.variableList[8].get())[1:],
                patientEmergencyContactPhoneNum=str(self.variableList[9].get())[1:], patientIllness=str(self.variableList[10].get())
            )
        else:
            self.sheet.sendPatientData(
                patientName=str(self.variableList[0].get()), patientGender=str(self.variableList[1].get()),
                patientBirth=str(self.variableList[2].get()), patientWeight=str(self.variableList[4].get())[:wlen - 3],
                patientHeight=str(self.variableList[5].get())[:hlen - 3],patientCreditId=str(self.variableList[6].get()),
                patientAddressPlace=str(self.variableList[7].get()),patientPhoneNum=str(self.variableList[8].get())[1:],
                patientEmergencyContactPhoneNum=str(self.variableList[9].get())[1:],patientIllness=str(self.variableList[10].get())
            )
        self.close = True
        self.eWindow.destroy()
        del self


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
        self.QRButton = tk.Button(self.oWindow, text="使用QR code", font=self.fontStyle, bg="white", command=self.QRcodeGetId)
        self.QRButton.grid(row=2, column=0, pady=2, padx=10)
        self.entryButton = tk.Button(self.oWindow, text="使用身分輸入", font=self.fontStyle, bg="white", command=self.EntryGetId)
        self.entryButton.grid(row=3, column=0, pady=2, padx=10)
        self.findButton = tk.Button(self.oWindow, text="確定", font=self.fontStyle, bg="white",command=self.findRecord)
        self.findButton.grid(row=4, column=0, pady=2, padx=10)

    def QRcodeGetId(self):
        self.QRScanWindow = QRcodeScan(self.oWindow, self.sheet, self.nameVariable, self.idVariable, self.QRsccan, self.QRidVar)

    def EntryGetId(self):
        self.entryWindow = IdEntry(self.oWindow, self.sheet, self.nameVariable, self.idVariable)

    def findRecord(self):
        if len(str(self.idVariable.get())) > 9:
            createRecordWindow(self.window, str(self.idVariable.get()), self.sheet)
            del self.QRScanWindow
            del self.entryWindow
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
        self.idLabel = tk.Label(self.QRWindow, textvariable=self.nameVar, font=self.fontStyle, bg="skyblue", anchor="center")
        self.idLabel.grid(row=0, column=0, pady=2, padx=10)
        self.idLabel = tk.Label(self.QRWindow, textvariable=self.idVar, font=self.fontStyle, bg="white", anchor="center")
        self.idLabel.grid(row=1, column=0, pady=2, padx=10)
        self.cButton = tk.Button(self.QRWindow, text="開始掃描", font=self.fontStyle, bg="white", command=self.scaning, anchor="center")
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
    buttonRe = tk.Button(window, text='j86', command=lambda: createRecordWindow(window, "J868686880", sheet))
    buttonRe.pack()
    buttonQR = tk.Button(window, text='zp4', command=lambda: createQRWindow(window, sheet, QRscan, QRid))
    buttonQR.pack()
    window.mainloop()


