import os
import boto3

DIR = os.path.dirname(os.path.realpath(__file__))


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
               text=open(f'{DIR}/templates/email.txt', 'r').read(),
               html=open(f'{DIR}/templates/email.html', 'r').read())
    print('Completed')
