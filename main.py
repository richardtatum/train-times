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
        timetable['status'] = x['status']
        timetable['platform'] = x['platform']
        timetable['dest'] = x['destination_name']
        timetable['sch_dep'] = x['aimed_departure_time']
        timetable['exp_dep'] = x['expected_departure_time']
        timetable['eta'] = get_arrival_time(x['service_timetable']['id'], dest_code)
        departures.append(timetable)

    format_email(departures, dep_name, dest_name)


def format_email(departures, dep_name, dest_name):
    with open('email/email.html', 'w') as f:
        header = f'''
                <h4>{dep_name} to {dest_name}</h3>
                <br>
                <br>
            '''
        f.write(header)

        for d in departures:
            html = f'''
                <b>{d["sch_dep"]} &nbsp; {d['dest']} &nbsp; &nbsp; &nbsp; Exp:{d['exp_dep']}</b>
                <p>Status: {d['status'].title()} &nbsp; &nbsp; Platform: {d['platform']}</p>
                <p>ETA {dest_name}: {d['eta']}</p>
                <br>
            '''
            f.write(html)

    send_timings_email()


def get_arrival_time(id, dest):
    r = requests.get(id)
    data = r.json()

    if 'error' in data:
        raise ValueError(data['error'])

    exp_arr_time = [li['expected_arrival_time'] for li in data['stops'] if li['station_code'] == dest.upper()]
    return exp_arr_time[0]


def send_email(subject='', text='', html=''):
    ses = boto3.client(
        'ses',
        region_name=os.getenv('SES_REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )        

    ses.send_email(
        Source=os.getenv('SES_EMAIL_SOURCE'),
        Destination={'ToAddresses': [os.getenv('SES_EMAIL_DEST')]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text},
                'Html': {'Data': html}
            }
        }
    )


def send_timings_email():
    send_email(subject='Train Times',
               text=open('email/email.txt', 'r').read(),
               html=open('email/email.html', 'r').read())
    print('Completed')


def send_afternoon_email():
send_morning_email()
