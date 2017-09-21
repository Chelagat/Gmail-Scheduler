from __future__ import print_function
from sys import argv
import time
import datetime
import httplib2
import googleapiclient
import os
# Import smtplib for the actual sending function
import base64
# Import the email modules we'll need
from email.mime.text import MIMEText

from apiclient import discovery
from oauth2client.file import Storage
from datetime import datetime, time
from time import sleep


import subprocess

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'sredmond'


def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(bytes(message.as_string()))
    raw = raw.decode()
    return {'raw': raw}

def wait_start(send_time):
    send_time= time(*(map(int, send_time.split(':'))))
    while send_time > datetime.today().time():
        sleep(1)

def send_message(service, user_id, message_body):
    try:
        #message = {'message': message_body}
        message= service.users().messages().send(userId=user_id, body= message_body).execute()
        return message
    except googleapiclient.errors.HttpError as error:
        print("An error occured, sredmond, ", error)

def retrieve_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir,
                               'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    return credentials

def set_up_message(title, body, recepient, send_time):
    wait_start(send_time)
    credentials = retrieve_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = create_message(recepient, title, body)
    draft = send_message(service, 'me', message)

if __name__ == '__main__':
    send_time, title, body, recipient = argv[1], argv[2], argv[3], argv[4]
    set_up_message(title, body, recipient, send_time)
