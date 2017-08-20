import twilio_secrets as ts

import re
import os
from twilio.rest import Client

class TwilioMessenger():
    
    MASTER_LIST_NUMBERS = 'master_list_phone_numbers.txt'
    NUMBERS_FROM_WEB_FORM = 'egret_phone'
    WEB_NUMBERS_LOCATION = '/home/jessicakam/Downloads'

    def __init__(self):
        self.account_sid = ts.ACCOUNT_SID
        self.auth_token = ts.AUTH_TOKEN
        self.SEND_FROM = ts.PHONE_NUMBER 
        self.SEND_TO = ''
        self.client = Client(self.account_sid, self.auth_token)

    def run(self):
        self.updateMasterListNumbers()
        self.getNumbers()
        self.getMsg()
        for number in self.numbers:
            self.SEND_TO = number
            self.sendMsg()

    def updateMasterListNumbers(self):
        path = TwilioMessenger.WEB_NUMBERS_LOCATION
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and 'egret_phone' in f]
        for f in files:
            file_path = os.path.join(path, f)
            with open(file_path, 'r') as new_number_file:
                with open(TwilioMessenger.MASTER_LIST_NUMBERS, 'a') as master_list:
                    phone_number = new_number_file.readline()
                    master_list.write(phone_number)
            os.remove(file_path)

    def getNumbers(self):
        self.numbers = []
        with open(TwilioMessenger.MASTER_LIST_NUMBERS, 'r') as f:
            for line in f:
                parsed_number = self.parseNumber(line)
                if parsed_number:
                    self.numbers.append(parsed_number)

    def parseNumber(self, line):
        number = ''
        pattern = '(.)*(\d{3})(.)*(\d{3})(.)*(\d{4})'
        phone_pattern = re.compile(pattern)
        results = phone_pattern.search(line)
        if results:
            results = results.groups()
            p1 = results[1]
            p2 = results[3]
            p3 = results[5]
        if results and p1 and p2 and p3:
            number = p1 + p2 + p3
        if number:
            return '+1' + number
        print('Number not valid')
        return ''

    def getMsg(self):
        self.msg = ''
        with open('predictions.txt', 'r') as f:
            for line in f:
                self.msg = self.msg + line + ' '

    def sendMsg(self):
        self.client.api.account.messages.create(to=self.SEND_TO,
                                           from_= self.SEND_FROM,
                                           body=self.msg)
        print('Sent msg to {0}'.format(self.SEND_TO))

if __name__=='__main__':
    tw = TwilioMessenger()
    tw.run()
