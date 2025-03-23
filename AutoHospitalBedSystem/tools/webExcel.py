import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    def __init__(self, key):

        scopes = ["https://spreadsheets.google.com/feeds"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes)

        client = gspread.authorize(credentials)

        self.sheet = client.open_by_key(key).sheet1

    def gsheet(self, data):

        self.sheet.append_row(data, 1)

    def next_available_row(self, worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list))


if __name__ == "__main__":

    key = '1GOXygfcCpxYwnqAKrDGk19pT-shsA-F4W9l2dllJIBM'
    sheet = Sheet(key)

    localtime = time.localtime()
    result = time.strftime("%Y/%m/%d %I:%M:%S %p", localtime)

    item = sheet.next_available_row(sheet.sheet)

    sheet.gsheet((result, f'Item{item}', 'Taiwan', 'ATCG'))


