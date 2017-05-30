from __future__ import print_function
import httplib2
import googleapiclient
import os
# Import smtplib for the actual sending function
import smtplib
import base64
# Import the email modules we'll need
from email.mime.text import MIMEText

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'client2'


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

def create_message(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	raw = base64.urlsafe_b64encode(bytes(message.as_string(), 'utf8'))
	raw = raw.decode()
	return {'raw': raw}


def create_draft(service, user_id, message_body):
	try:
		message = {'message': message_body}
		draft = service.users().drafts().create(userId=user_id, body=message).execute()
		print ('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
		return draft
	except googleapiclient.errors.HttpError as error:
		print ("An error occured", error)
		return None


def main():
	credentials = get_credentials()
	print("credential: ", credentials)
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	results = service.users().labels().list(userId='me').execute()
	labels = results.get('labels', [])
	if not labels:
		print('No labels found.')
	else:
		print('Labels:')
		for label in labels:
			print(label['name'])



if __name__ == '__main__':
    main()
    credentials = get_credentials()
    print("credential: ", credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = create_message("norahborus68@gmail.com", "nnegrete@stanford.edu", "Testing script", "Test! Test!")
    draft = create_draft(service, 'me', message)
    print(draft)

