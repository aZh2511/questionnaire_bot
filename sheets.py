import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import types
from datetime import datetime


def connect():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    log_info = ServiceAccountCredentials.from_json_keyfile_name("settings.json", scope)

    client = gspread.authorize(log_info)

    sheet = client.open("Telegram_Bot_Andrew").sheet1

    return sheet


def insert_answer(data: list):
    sheet = connect()
    user = types.User.get_current()
    now = datetime.now()

    for i in range(len(data)):
        to_insert = [
            user.full_name,                 # Fullname
            user.username,                  # Username
            data[i][0],                     # Question
            data[i][1],                     # Answer
            now.date().isoformat()          # Time
        ]
        sheet.insert_row(to_insert, 2)
