#!/usr/bin/env python3

# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import logging
import time
import sys

### USER CONFIGURATION ###
REALLY_DO_IT=False
SEARCH_STRING='older:1/7/2023 -label:IMPORTANT is:unread -is:starred'

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']
SECRETS_FILE='client_secret.json'





#logging.basicConfig(level=logging.DEBUG)
logging.getLogger('googleapiclient').setLevel(logging.INFO)

logger = logging.getLogger('ewa_email_cleanup')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

record_everything=logging.FileHandler(filename='message_details.log')
console_output=logging.StreamHandler()

record_everything.setFormatter(formatter)
#console_output.setFormatter(formatter)

record_everything.setLevel(logging.DEBUG)
console_output.setLevel(logging.INFO)

logger.addHandler(record_everything)
logger.addHandler(console_output)

def getEmails():
        # Variable creds will store the user access token.
        # If no valid token found, we will create one.
        creds = None

        # The file token.pickle contains the user access token.
        # Check if it exists
        if os.path.exists('token.pickle'):
            logger.debug('Token file exists')
            
            # Read the token from the file and store it in the variable creds
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                logger.debug('Token file contents: {}'.format(creds))
                
        # If credentials are not available or are invalid, ask the user to log in.
        if not creds or not creds.valid:
                logger.debug('Credentials missing or not valid')
                if creds and creds.expired and creds.refresh_token:
                        logger.debug('Refreshing token')
                        creds.refresh(Request())
                else:
                        logger.debug("Doing flow thing")
                        flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
                        creds = flow.run_local_server(port=0)

                # Save the access token in token.pickle file for the next run
                with open('token.pickle', 'wb') as token:
                        logger.debug('Writing credentials: {}'.format(creds))
                        pickle.dump(creds, token)

        # Connect to the Gmail API
        service = build('gmail', 'v1', credentials=creds)


        batch_ct=0
        msg_ct=0

        # request a list of all the messages
        last_page_p = False
        pageToken=None

        if REALLY_DO_IT:
            sys.stderr.write("REALLY_DO_IT is set.\nIf you don't trust this script to make bulk changes to your e-mails, hit CTL-C immediately!")
            sys.stderr.flush()
            time.sleep(10)
            sys.stderr.write(" Proceeding.\n")
            sys.stderr.flush()
        else:
            sys.stderr.write("REALLY_DO_IT is NOT set.  This run is for testing purposes only and will not actually make any changes.\n")

        logger.info('Running with search string \'{}\''.format(SEARCH_STRING))
        logger.debug('Starting new run with REALLY_DO_IT={}'.format(REALLY_DO_IT))
        
        while not last_page_p:
            result = service.users().messages().list(userId='me',
                                                     maxResults=500,
                                                     pageToken=pageToken,
                                                     q=SEARCH_STRING,
                                                     ).execute()
            #logger.debug("Result: '{}'".format(result))
            try:
                pageToken=result['nextPageToken']
            except KeyError:
                pageToken=None
                last_page_p=True

            if result['resultSizeEstimate']==0:
                logger.info('No messages matching search string found (at least on this page)!')
                break
            
            batch_ct = batch_ct + 1
            logger.info('Message list: {} messages, next page token {}'.format(len(result['messages']), pageToken))
            messages = result.get('messages')
        
            to_mark_read=[]
           
            for msg in messages:
                # Get the message from its id
                to_mark_read.append(msg['id'])
                msg_ct = msg_ct+1
                continue
        
            if REALLY_DO_IT:
                logger.debug("DOING mark as read: {}".format(to_mark_read))
                try:
                    cmd_body = {
                        'ids': to_mark_read,
                        'removeLabelIds': ['UNREAD']
                    }
                    result=service.users().messages().batchModify(userId='me', body=cmd_body).execute()
                    logger.debug("result: {}".format(result))
                except:
                    logger.exception("That didn't work")
                    raise
                
            else:
                logger.debug("WOULD mark as read: {}".format(to_mark_read))
    
        logger.info("Done: {} batches, with a total of {} messages".format(batch_ct, msg_ct))

getEmails()
