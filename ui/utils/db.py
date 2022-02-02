import os
import gspread
import pandas as pd
from pprint import pprint
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

#Cambiamos directorio de trabajo al directorio del archivo para poder abrir el .json de credenciales
fileDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(fileDir)

"""
Variables globales:
- scope: Alcance de nuestra aplicacion, APIs a usar (Google SpreadSheets y Drive)
- spreadsheet: Nombre del Libro de Calculo 
- spreadsheet_id: Identificador de nuestro Libro de Calculo
- sheet: Nombre de la Hoja a modificar (hoja de validacion)
- creds: Credenciales de la cuenta
"""
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
spreadsheet = "MuHeQa_Validation"
spreadsheet_id = "1TY6Tj1OwITOW3o1nYRFFRY1bunvHNImUj-J0omRq4-I"
sheet = "Validation"

if os.path.exists('credentials.json'):
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
else:
    print("DB ERROR > Missing Credentials for accessing")
    exit()

def connectToSheet():
    """
    Funcion auxiliar que abre la Hoja de Validacion de nuestro Libro 
    """
    service = build("sheets","v4",credentials=creds)
    return service.spreadsheets()

def insertRow(sheet):
    """
    Funcion auxiliar que inserta una nueva fila en la Hoja de Validacion
    """
    pass

def getQuestionsInSheet(sheet):
    """
    Funcion auxiliar que obtiene todas las preguntas en una determinada hoja
    Sea esta hoja un dataset de EQA que sigue nuestro formato
    """
    client = gspread.authorize(creds)
    sheetClient = client.open("MuHeQa_Validation").worksheet(sheet)
    records = sheetClient.get_all_records()
    questions = []
    for i in records:
        questions.append(i["question"])
    return questions