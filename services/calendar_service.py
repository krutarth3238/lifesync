from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    creds = None

    if os.path.exists('token_calendar.pickle'):
        with open('token_calendar.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token_calendar.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_calendar_events(date: str = None) -> dict:
    try:
        service = get_calendar_service()

        if not date:
            import datetime
            date = datetime.datetime.utcnow().strftime('%Y-%m-%d')

        start = f"{date}T00:00:00Z"
        end = f"{date}T23:59:59Z"

        events_result = service.events().list(
            calendarId='primary',
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return {"events": [], "message": f"No events on {date}"}

        result = []
        for e in events:
            result.append({
                "title": e.get('summary', 'No Title'),
                "start": e['start'].get('dateTime', e['start'].get('date')),
                "end": e['end'].get('dateTime', e['end'].get('date'))
            })

        return {"events": result}

    except Exception as ex:
        return {"error": str(ex), "service": "Google Calendar"}