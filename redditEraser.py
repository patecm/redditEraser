#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 2021

@author: AmbitiousDonut

for more info see:
"""
import praw
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import argparse

'''
Edit the variables below this to match your Reddit credentials and save the file
These can be found at https://ssl.reddit.com/prefs/apps/
'''
clientID = 'YourCodeHere'
clientSecret = 'YourSecretIDHere'
userName = 'AmbitiousDonut'
password = 'MyTotallyRealPassword'
agent = 'commentEditor'

'''
Dont mess with things below this point
'''
#warnings.filterwarnings("ignore", category=DeprecationWarning)
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--minkarma',
                    action='store',
                    help="Delete comments with less karma than this. Default is 0.",
                    type=int,
                    default=0)
parser.add_argument('--age',
                    help="Delete comments older than this (in days). Default is 7 days.",
                    type=int,
                    default=90)
# Parse the argument
args = parser.parse_args()

# Log in
reddit = praw.Reddit(user_agent= agent,
                     client_id=clientID, client_secret=clientSecret,
                     username=userName, password=password,
                     check_for_updates=False)
# Set the read/write access to the accoun
reddit.read_only = False
# Create a user instance
redditor = reddit.redditor(userName)

print('\nTotal karma for {}: {}'.format(userName, redditor.comment_karma))
print('\nDeleting comments older than {} days and below {} karma'.format(args.age, args.minkarma))
proceed = input("Procede? y/n \n")
proceed = proceed.lower()
if 'y' in proceed:
    total_processed = 0
    total_deleted = 0
    deltaT = datetime.now() - relativedelta(days=args.age)
    for comment in redditor.comments.top(limit=1000):
        commentTime = datetime.utcfromtimestamp(comment.created_utc)
        if commentTime < deltaT :
            if total_processed % 100 == 0: 
                print('...{} comments processed...'.format(total_processed))
            if comment.score < args.minkarma :
                #comment.edit('     ')
                comment.delete()
                time.sleep(1)
                total_deleted += 1
            total_processed += 1
    if total_processed == 1000:
        print('PRAW limit of 1000 comments per instance reached')
    print('\n{} comments processed'.format(total_processed))
    print('{} comments deleted'.format(total_deleted))
    
else:
    print('Canceling operation...')
    