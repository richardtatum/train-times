import requests
import os
from dotenv import load_dotenv
import boto3
load_dotenv()


def show_departures(dep, dest_code):
    URL = f'https://transportapi.com/v3/uk/train/station/{dep}/live.json'
    PARAMS = {
        'app_id': os.getenv('app_id'),
        'app_key': os.getenv('app_key'),
        'calling_at': dest_code,
        'station_detail': 'calling_at',
        'from_offset': '-PT00:30:00',
        'to_offset': 'PT03:00:00'
    }
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    if 'error' in data:
        raise ValueError(data['error'])

    dep_name = data['station_name']
    dest_name = data['departures']['all'][0]['station_detail']['calling_at'][0]['station_name']

    return format_data(dep_name, dest_name, dest_code, data['departures']['all'])


def format_data(dep_name, dest_name, dest_code, data):
    departures = []
    for x in data:
        timetable = {}
        timetable['Status'] = x['status']
        timetable['Platform'] = x['platform']
        timetable['Destination'] = x['destination_name']
        timetable['Scheduled Departure'] = x['aimed_departure_time']
        timetable['Expected Departure'] = x['expected_departure_time']
        timetable['Estimated Arrival Time'] = get_arrival_time(x['service_timetable']['id'], dest_code)
        departures.append(timetable)

    print(f'From {dep_name} to {dest_name}')
    for x in departures:
        print(x)
    send_morning_email(['rtatum@pm.me'])
    return departures


def get_arrival_time(id, dest):
    r = requests.get(id)
    data = r.json()

    if 'error' in data:
        raise ValueError(data['error'])

    exp_arr_time = [li['expected_arrival_time'] for li in data['stops'] if li['station_code'] == dest.upper()]
    return exp_arr_time[0]


def send_email(recipients, sender=None, subject='', text='', html=''):
    ses = boto3.client(
        'ses',
        region_name=os.getenv('SES_REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    if not sender:
        sender = os.getenv('SES_EMAIL_SOURCE')

    ses.send_email(
        Source=sender,
        Destination={'ToAddresses': recipients},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text},
                'Html': {'Data': html}
            }
        }
    )


def send_morning_email(email):
    send_email(recipients=email,
               subject='Morning Trains',
               text="test text",
               html="test <b>html</b>")
    print('Completed')


def send_afternoon_email(email):
    send_email(recipients=email,
               subject='Evening Trains',
               text=open('email/email.txt', 'r'),
               html=open('email/email.html', 'r'))


# show_departures('fnb', 'clj')
send_morning_email(['rtatum@pm.me'])
