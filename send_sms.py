import twilio_secrets as ts

import re
import os
from twilio.rest import Client

class SMSMessenger():
    
    MASTER_LIST_NUMBERS = 'master_list_phone_numbers.txt'
    MASTER_LIST_UNSUBSCRIBED = 'master_list_unsubscribed_numbers.txt'
    NUMBERS_TO_SUBSCRIBE = 'egret_phone'
    NUMBERS_TO_UNSUBSCRIBE = 'egret_unsubscribe_numbers'
    WEB_NUMBERS_LOCATION = '/home/jessicakam/Downloads'

    def __init__(self):
        self.account_sid = ts.ACCOUNT_SID
        self.auth_token = ts.AUTH_TOKEN
        self.SEND_FROM = ts.PHONE_NUMBER 
        self.SEND_TO = ''
        self.client = Client(self.account_sid, self.auth_token)
        self.master_list = []

    def run(self):
        self.updateMasterList()
        self.getMsg()
        for number in self.master_list:
            print('number: {0}'.format(self.master_list))
            self.SEND_TO = number
            self.sendMsg()

    def updateMasterList(self):
        self.saveOldMasterList()
        self.addSubscribers()
        self.removeUnsubscribers()
        self.createNewMasterList()
        
    def saveOldMasterList(self):
        print('Saving old master list...')
        self.path = SMSMessenger.WEB_NUMBERS_LOCATION
        # save current master list, assuming numbers in master list are correctly formatted
        if not os.path.exists(SMSMessenger.MASTER_LIST_NUMBERS):
            os.makedirs(SMSMessenger.MASTER_LIST_NUMBERS)
        with open(SMSMessenger.MASTER_LIST_NUMBERS, 'r') as master_list:
            #for line in master_list:
            #    self.master_list.append(line)
            self.master_lst = master_list.readlines()
        print(self.master_list)
            
    def addSubscribers(self):
        print('Adding new subscribers...')
        files_to_subscribe = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f)) and SMSMessenger.NUMBERS_TO_SUBSCRIBE in f]
        for f in files_to_subscribe:
            file_path = os.path.join(self.path, f)
            with open(file_path, 'r') as new_number_file:
                phone_number = new_number_file.readline()
                parsed_number = self.parseNumber(phone_number)
                if parsed_number:
                    self.master_lst.append('+1' + phone_number)
            os.remove(file_path)
        print(self.master_list)
            
    def removeUnsubscribers(self):
        print('Removing unsubscribers...')
        files_to_unsubscribe = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f)) and SMSMessenger.NUMBERS_TO_UNSUBSCRIBE in f]
        lst_to_unsubscribe = []
        for f in files_to_unsubscribe:
            file_path = os.path.join(self.path, f)
            with open(file_path, 'r') as new_number_file:
                unsubscribe_number = new_number_file.readline()
                parsed_number = self.parseNumber(unsubscribe_number)
                if parsed_number:
                    lst_to_unsubscribe.append('+1' + unsubscribe_number)
                # also save to master unsubscribe list
                with open(SMSMessenger.MASTER_LIST_UNSUBSCRIBED, 'a') as f:
                    f.write('+1' + unsubscribe_number + '\n') 
            os.remove(file_path)
        for unsubscriber in lst_to_unsubscribe:
            if unsubscriber in self.master_lst:
                self.master_lst.remove(unsubscriber)
        print(self.master_list)
        
    
    def createNewMasterList(self):
        print('Creating a new master list...')
        with open(SMSMessenger.MASTER_LIST_NUMBERS, 'w') as master_list:
            for number in self.master_lst:
                master_list.write(number + '\n')

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
            return number
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
    tw = SMSMessenger()
    tw.run()
