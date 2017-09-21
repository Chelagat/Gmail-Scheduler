from __future__ import print_function
import httplib2
import googleapiclient
import os
# Import smtplib for the actual sending function
import smtplib
import base64
# Import the email modules we'll need
from email.mime.text import MIMEText
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from threading import Thread
from datetime import datetime, time
from time import sleep
import pickle

from ast import literal_eval
import subprocess

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'sredmond'

from oauth2client.client import AccessTokenCredentials

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()
        print ('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
        return draft
    except googleapiclient.errors.HttpError as error:
        print ("An error occured", error)
        return None

#proper credit for this method goes to Artsiom Rudzenka of Stack Overflow, 
#who answered this on this thread:
#https://stackoverflow.com/questions/6579127/delay-a-task-until-certain-time
def wait_start(send_time):
    send_time= time(*(map(int, send_time.split(':'))))
    while send_time > datetime.today().time():
        sleep(1)

def get_body():
    read_from_file= raw_input("Enter F to read body from a file or C to enter your message into the console: ").upper()
    while (not read_from_file) or read_from_file not in ['F', 'C']:
        read_from_file= raw_input("Enter F to read body from a file or C to enter your message into the console: ").upper()
    if read_from_file== 'C':
        return raw_input("Type your message: ")
    else:
        file_path= raw_input("What is the complete file path of the message? ")
        message= None
        with open(file_path) as file:
            message= file.read()
        return message

if __name__ == '__main__':
    print("Welcome to our Gmail Script.")
    credentials = get_credentials()
    print (type(credentials))
    recipient = raw_input("Type in the recepient of the email: ")
    body = get_body()
    title = raw_input("Type in the title: ")
    send_time = raw_input("Input send time as military time (e.g. 15:20 for 3:20pm): ")
    p = subprocess.Popen(['python', 'set-up-service.py',send_time, title, body, recipient], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print ("Email scheduled!")

