from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import webreg_event

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Create a new calendar for the convenience of testing 
    calendar = {
        'summary': 'Schedule 1',
        'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    cal_id = created_calendar['id']
    print(cal_id)

    # Get events from pasteboard
    events_to_add = webreg_event.generate_events_from_pasteboard()
    for event in events_to_add:
        recurring_event = service.events().insert(calendarId=cal_id, body=event).execute()
        print(recurring_event['id'])

if __name__ == '__main__':
    main()
