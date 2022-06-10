import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

#Path to the credentials file
credentialsPath = './utils/credentials.json'

class SpreadManager:

    def __init__(self,spreadsheet, spreadsheetId, validationSheet):
        """
        Class constructor
        """
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.spreadsheet = spreadsheet
        self.spreadsheetId = spreadsheetId
        self.validationSheet = validationSheet
        
        if os.path.exists(credentialsPath):
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, self.scope)
            self.service = build("sheets","v4",credentials=self.creds, cache_discovery=False)
            self.connector = self.service.spreadsheets()
        else:
            print("DB ERROR > Missing Credentials for accessing")
            exit()

    def insertRow(self, row):
        """
        Method that inserts a row into the spreadsheet    
        """
        values = (
            self.connector.values().append(
                spreadsheetId=self.spreadsheetId,
                range=f"{self.validationSheet}!A:E",
                body=dict(values=row),
                valueInputOption="USER_ENTERED",
            ).execute()
        )