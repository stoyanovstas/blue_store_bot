import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleClient:
    def __init__(self, json_path, sheet_id):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(sheet_id).worksheet("CRM")

    def find_user(self, telegram_id):
        records = self.sheet.get_all_records()
        for row in records:
            if str(row.get("Telegram ID")) == telegram_id:
                return row
        return None

    def register_user(self, telegram_id, name):
        self.sheet.append_row([telegram_id, name, "", 0, "", "", ""])