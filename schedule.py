from __future__ import print_function
import datetime
import pickle
import os.path
# import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from flask import Flask, request, abort
import os

app = Flask(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



def show_schedule():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    pushtext = ''
    w_list = ['月', '火', '水', '木', '金', '土', '日']

    for i in range(1, 4):

        tommorow = datetime.datetime.utcnow() + datetime.timedelta(days = i)
        start = tommorow.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        end = tommorow.replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + 'Z'

        events_result = service.events().list(calendarId='nl0d8pbk4spklbp2r4r7tbsglg@group.calendar.google.com', 
                                            timeMin=start, timeMax=end,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        pushtext_tmp = '【' + str(int(start[5:7])) + '/' + str(int(start[8:10])) + '(' + w_list[tommorow.weekday()] + ')】'

        if not events:
            pushtext_tmp += '\n予定がありません'
        for event in events:
            if 'date' in event['start'].keys():
                if event['start']['date'] == tommorow.strftime('%Y-%m-%d'):
                    pushtext_tmp += '\n[' + event['summary'] + ']'
            
            else:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                pushtext_tmp += '\n' + start[11:16] + '~' + end[11:16] + ' ' + event['summary']

        pushtext += pushtext_tmp + '\n\n'

    pushtext = pushtext[:-2]
    print(pushtext)
    return pushtext

if __name__ == "__main__":
    show_schedule()