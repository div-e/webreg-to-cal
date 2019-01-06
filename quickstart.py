from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    # Create a new calendar for the convenience of testing 
    calendar = {
        'summary': 'Test Calendar 2',
        'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    cal_id = created_calendar['id']
    print(cal_id)

    # Try adding sample event
    sample_event = {
        'summary': 'MATH 171A LE',
        # 'location': '800 Howard St., San Francisco, CA 94103',
        # 'location': "PCYNH 106",
        # 'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            # Instead of '2018-09-07T13:50:00-07:00'
            # 'America/Los_Angeles' has daylight saving, so we will not use
            #   dateTime with fixed offset
            'dateTime': '2018-09-07T13:00:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2018-09-07T13:50:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            # MWF
            # Instruction ends: Friday, March 15 (2019)
            # Note that the time is in "Z" (which is "UTC")
            #   we intend the end date to be 11:59pm one day later,
            #   Saturday, March 16 (2019) in UTC Time
            "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20190316T235959Z"
        ]
    }

    recurring_event = service.events().insert(calendarId=cal_id, body=sample_event).execute()

    print(recurring_event['id'])


if __name__ == '__main__':
    main()
