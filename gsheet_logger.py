import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheet configuration
SHEET_ID = "1877HyaqZEYgz18V3hYxK8uU39cdK0ZV0QyFkRGtQ274"
SHEET_NAME = "SmallSignalAnalysis_Logging"

def log_interaction(credentials_path, ip_address, case_title, source):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, ip_address, case_title, source])
    except Exception as e:
        print(f"Logging failed: {e}")
