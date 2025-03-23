import gspread
# import requests
import datetime
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from UploadImgModule.Upload_Image_Module import ImgMaster
# from UploadImgModule.Upload_Image_Module import ImgMaster
# from ..UploadImgModule.Upload_Image_Module import ImgMaster
from QRCodeModule import MakeQRCode


class Sheet:
    def __init__(self):
        self.scopes = ["https://spreadsheets.google.com/feeds"]

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Liu Ty\Desktop\newHospitalBed\webExcel\credentials.json", self.scopes)

        self.client = gspread.authorize(self.credentials)

        self.sheet = self.client.open_by_key("1GOXygfcCpxYwnqAKrDGk19pT-shsA-F4W9l2dllJIBM").sheet1

        self.imgMaster = ImgMaster()

        self.qrCodeMaker = MakeQRCode()

    def gSheet(self, data):
        self.sheet.append_row(data, 1)

        # print(self.sheet.id)

    def getNewId(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        row_id = len(str_list)
        return row_id

    def sendPatientData(self, **kwargs):
        now = str(datetime.datetime.now())
        date = datetime.date.today()
        year = date.year
        age = str(int(year) - int(kwargs["patientBirth"][:4]))
        str_list = list(filter(None, self.sheet.col_values(1)))
        row_id = len(str_list)
        self.sheet.append_row((now, row_id, kwargs["patientName"], kwargs["patientGender"], kwargs["patientBirth"], age, kwargs["patientWeight"], kwargs["patientHeight"], kwargs["patientCreditId"], kwargs["patientAddressPlace"], kwargs["patientPhoneNum"], kwargs["patientEmergencyContactPhoneNum"], kwargs["patientIllness"]), 1)
        del now, date, year, age, str_list, row_id

    def saveSheetData(self, filePath, index=False, verbose=False):
        self.getSheetData(verbose=verbose)
        self.df.to_csv(filePath, index=index)

    def getSheetData(self, verbose=False):
        self.df = pd.DataFrame(data=self.sheet.get_all_records())
        if verbose:
            print(self.df)
        return self.df

    def findSheetValue(self, key, value):
        self.getSheetData()
        try:
            index = int(self.df.index[self.df[key] == value].values[0])
        except Exception as e:
            print("[INDEX ERROR] Cannot Find The Value")
            # print(e)
            return 99999, False

        return index, True

    def convertCsvToListData(self, csvFile, verbose=False):
        df = pd.read_csv(csvFile)
        recordData = df.to_numpy().tolist()
        if verbose:
            print(recordData)
        return recordData

    def updateWholeSheetData(self, allData):
        str_list = list(filter(None, self.sheet.col_values(1)))
        row_num = len(str_list) - 1
        for i in range(row_num):
            self.sheet.update(f"A{i + 2}:M{i + 2}", [
                [allData[i]]
            ])

    def getRowSheetData(self, row, verbose=False):
        row += 2
        data = self.sheet.row_values(row)
        if verbose:
            print(data)
        return data

    def getColSheetData(self, col, verbose=False):
        col += 2
        data = self.sheet.col_values(col)
        if verbose:
            print(data)
        return data

    def getColSheetImage(self, col, saveFolder):
        data = self.getColSheetData(col)
        imgUrl = str(data["patientCreditIdQRCode"])
        name = str(data["patientCreditId"])
        self.imgMaster.getImageFromUrl(imgUrl, saveFolder, f'{name}.png')
        img = self.imgMaster.readImageFromSaveFile(saveFolder, f'{name}.png')
        return img

    def uploadImageUrl(self, col, url):
        col += 2
        self.sheet.update_acell(f"N{col}", url)

    def uploadPatientPhotoUrl(self, col, url):
        col += 2
        self.sheet.update_acell(f"O{col}", url)

    def makeAllCreditIdQRCodes(self, saveFolder, verbose=False):
        self.getSheetData()
        creditIds = self.df["patientCreditId"].copy().tolist()
        if verbose:
            print(creditIds)
        self.qrCodeMaker.runMultipleQRCodes(creditIds, saveFolder, True)

    def uploadPatientPhoto(self, fileName):
        uploadData = self.imgMaster.uploadImageFromFile(fileName)
        index, isFind = self.findSheetValue("patientCreditId", uploadData.title[len(uploadData.title) - 14:len(uploadData.title) - 4])
        if isFind:
            self.uploadPatientPhotoUrl(index, uploadData.link)

    def uploadPatientPhotos(self, path):
        self.imgMaster.uploadImageFromPath(path)
        self.uploadAllPhotoImgUrlFromJson(path, path)

    def uploadAllPhotoImgUrlFromJson(self, jsonPath, saveImgPath):
        self.patientPhoto = self.imgMaster.getImageUrlFromDefaultJson(jsonPath, saveImgPath)
        for img in self.patientPhoto:
            name = img[0]
            url = img[1]
            index, isFind = self.findSheetValue("patientCreditId", name)
            if isFind:
                self.uploadPatientPhotoUrl(index, url)

    def uploadAllCreditQRCodesFromJson(self, jsonPath, saveImgPath):
        self.imgDetail = self.imgMaster.getImageUrlFromDefaultJson(jsonPath, saveImgPath)
        for img in self.imgDetail:
            name = img[0]
            url = img[1]
            index, isFind = self.findSheetValue("patientCreditId", name)
            if isFind:
                self.uploadImageUrl(index, url)

    def uploadAllCreditQRCodesToSheet(self, QRCodeFolder):
        imgList = self.imgMaster.uploadImageFromPath(QRCodeFolder)
        # print(imgList)
        for img in imgList:
            print(img.title[len(img.title) - 14:len(img.title) - 4], img.link)
            index, isFind = self.findSheetValue("patientCreditId", str(img.title[len(img.title) - 14:len(img.title) - 4]))
            if isFind:
                self.uploadImageUrl(index, str(img.link))

    def updateSpecificSheetData(self, index, **kwargs):
        now = str(datetime.datetime.now())
        date = datetime.date.today()
        year = date.year
        age = str(int(year) - int(kwargs["patientBirth"][:4]))
        self.sheet.update(f"A{index + 2}:M{index + 2}", [
            [now, index, kwargs["patientName"], kwargs["patientGender"], kwargs["patientBirth"], age, kwargs["patientWeight"], kwargs["patientHeight"], kwargs["patientCreditId"], kwargs["patientAddressPlace"], kwargs["patientPhoneNum"], kwargs["patientEmergencyContactPhoneNum"], kwargs["patientIllness"]]
        ])


if __name__ == "__main__":
    sheet = Sheet()
    # sheet.makeAllCreditIdQRCodes(r'D:\Programing\webExcel\creditQRCodes')
    # sheet.uploadAllCreditQRCodesToSheet(r'D:\Programing\webExcel\creditQRCodes')
    # sheet.uploadAllCreditQRCodesFromJson(r'D:\Programing\webExcel\creditQRCodes', r'D:\Programing\webExcel\creditQRCodes')
    # sheet.uploadPatientPhotos(r'D:\Programing\Opencv\JetsonNano_Projects\newHospitalBed\webExcel\patientPhoto')
    sheet.uploadPatientPhoto(r"C:\Users\Hding49\Downloads\H106378143.png")
    # sheet.getSheetData()

    # index, isFind = sheet.findSheetValue("patientCreditId", "A123456789")
    # if isFind:
    #     sheet.updateSpecificSheetData(
    #         index,
    #         patientName="ktliu", patientGender="male", patientBirth="2005/1/24",
    #         patientWeight="70", patientHeight="180", patientCreditId="A123456780",
    #         patientAddressPlace="台北市內湖區", patientPhoneNum="912345678",
    #         patientEmergencyContactPhoneNum="923456789", patientIllness="急性腦殘",
    #         patientCreditIdQRCode=''
    #     )

    # print(sheet.getColSheetData(1))

    # sheet.saveSheetData("./patientData.csv", index=False, verbose=True)
    # listData = sheet.convertCsvToListData("./patientData.csv", True)
    # sheet.updateWholeSheetData(listData)
    # df = pd.read_csv("./patientData.csv")
    # print(df)

    # sheet.sendPatientData(
    #     patientName="tychen", patientGender="female", patientBirth="2005/06/09",
    #     patientWeight="45", patientHeight="153", patientCreditId="L256987336",
    #     patientAddressPlace="新北市樹林區", patientPhoneNum="900587633",
    #     patientEmergencyContactPhoneNum="921876335", patientIllness="COVID-19",
    #     patientCreditIdQRCode=''
    # )


