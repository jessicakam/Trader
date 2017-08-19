# /usr/bin/env python

import twilio_secrets as ts

import requests
from requests.auth import HTTPBasicAuth
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = ts.ACCOUNT_SID #'AC1e840b5654d8c87fbf2eff3264cd5007' #ts.ACCOUNT_SID
auth_token = ts.AUTH_TOKEN #'01f9ab14e8b8a6aa0e769eb00ec4c9f8' #ts.AUTH_TOKEN
SEND_FROM = '+16266843715' #'+15005550006' #ts.PHONE_NUMBER #'+16268251248'
SEND_TO = '+16268251248' #'+5104802511'

print(account_sid)
print(auth_token)
print(SEND_FROM)
print(SEND_TO)

#r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
#r = requests.get('https://api.gi', auth=HTTPBasicAuth('user', 'pass'))
#print('r status code: {0}'.format(r.status_code))

client = Client(account_sid, auth_token)

message = client.api.account.messages.create(to=SEND_TO,
                                             from_= SEND_FROM,
                                             body="WAKE UP BIETCH (w/o 1)")
