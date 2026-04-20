from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle, datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    creds = None

    if os.path.exists('token_sheets.pickle'):
        with open('token_sheets.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token_sheets.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def append_to_sheet(task: str, priority: str = "Medium") -> dict:
    try:
        service = get_sheets_service()
        sheet_id_file = 'sheet_id.txt'

        # Check if sheet already exists
        if os.path.exists(sheet_id_file):
            with open(sheet_id_file) as f:
                spreadsheet_id = f.read().strip()
        else:
            spreadsheet = service.spreadsheets().create(body={
                'properties': {'title': 'LifeSync Planner'},
                'sheets': [{'properties': {'title': 'Tasks'}}]
            }).execute()

            spreadsheet_id = spreadsheet['spreadsheetId']

            with open(sheet_id_file, 'w') as f:
                f.write(spreadsheet_id)

            # Add header only once
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range='Tasks!A1',
                valueInputOption='RAW',
                body={'values': [['Timestamp', 'Task', 'Priority']]}
            ).execute()

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Tasks!A1',
            valueInputOption='RAW',
            body={'values': [[timestamp, task, priority]]}
        ).execute()

        return {
            "status": "success",
            "message": f"Task '{task}' logged"
        }

    except Exception as ex:
        return {"error": str(ex), "service": "Google Sheets"}