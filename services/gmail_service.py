from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None

    if os.path.exists('token_gmail.pickle'):
        with open('token_gmail.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token_gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_unread_emails(max_results: int = 5) -> dict:
    try:
        service = get_gmail_service()

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX', 'UNREAD'],
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return {"emails": [], "message": "No unread emails"}

        emails = []

        for msg in messages:
            txt = service.users().messages().get(
                userId='me', id=msg['id']).execute()

            headers = txt['payload']['headers']

            subject = next(
                (h['value'] for h in headers if h['name'] == 'Subject'),
                'No Subject'
            )

            sender = next(
                (h['value'] for h in headers if h['name'] == 'From'),
                'Unknown'
            )

            emails.append({
                "from": sender,
                "subject": subject
            })

        return {"emails": emails}

    except Exception as ex:
        return {"error": str(ex), "service": "Gmail"}