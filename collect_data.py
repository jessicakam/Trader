# 2017/08/06
import gdax
import csv
import os
from datetime import datetime, timedelta
from optparse import OptionParser


class CollectData():

    #TODO - maybe include irregular data from 2016/05/18 - 2016/05/24
    SAMPLING_INTERVAL = 5
    INTERVAL_MULTIPLIER = 60
    DATE_FORMAT = '%Y/%m/%d'
    
    def __init__(self, **kwargs):
        self.public_client = gdax.PublicClient()
        today = datetime.utcnow()
        self.conversion_interested_in = 'ETH-USD'
        
        self.start_date = today.strftime(CollectData.DATE_FORMAT)
        self.end_date = today.strftime(CollectData.DATE_FORMAT)
        if kwargs.get('date'):           
            self.start_date = kwargs.get('date')
            self.end_date = kwargs.get('date')
        if kwargs.get('start_date') and kwargs.get('end_date'):
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
        
        self.sampling_interval = CollectData.SAMPLING_INTERVAL * CollectData.INTERVAL_MULTIPLIER
        if kwargs.get('sampling_interval'):
            self.sampling_interval = int(kwargs.get('sampling_interval')) * CollectData.INTERVAL_MULTIPLIER
        
    def run(self):
        self.generateListDates()
        for date in self.lst_dates:
            self.date = date
            print('running for {0}'.format(self.date))
            self.queryData()
            self.generateOutputFilename()
            self.makeFolders()
            print('output_file: {0}'.format(self.output_file))
            self.writeData()
        
    def dateStringToObject(self, date_string):
        return datetime.strptime(date_string, CollectData.DATE_FORMAT)
        
    def dateObjectToString(self, date_object):
        return date_object.strftime(CollectData.DATE_FORMAT)
        
    def generateListDates(self):
        start = self.start_date
        end = self.end_date
        self.lst_dates = []
        while start <= end:
            self.lst_dates.append(start)
            start_obj = self.dateStringToObject(start) + timedelta(days=1)
            start = self.dateObjectToString(start_obj)
        
    def queryData(self):
        start_str = self.dateStringToIsoString(self.date)
        next_day_obj = self.dateStringToObject(self.date) + timedelta(days=1)
        end_str = self.dateStringToIsoString(self.dateObjectToString(next_day_obj))
        self.data = self.public_client.get_product_historic_rates(self.conversion_interested_in, start=start_str, end=end_str, granularity=self.sampling_interval)
        print('len of self.data: {0}'.format(len(self.data)))

        if len(self.data) > 60*60*24 / self.sampling_interval:
            print('got strange number of results')
            self.data = []
        
    def writeData(self):
        csv_header = ['time', 'low', 'high', 'open', 'close', 'volume']
        with open(self.output_file, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(csv_header)
            for line in self.data:
                csv_writer.writerow(line)
                
    def dateStringToIsoString(self, date):
        date_obj = self.dateStringToObject(date)
        return date_obj.isoformat()
    
    def generateOutputFilename(self):
        self.output_file = os.path.join('data',
                                'eth',
                                self.date,
                                'gdax.csv')
    def makeFolders(self):
        year, month, day = self.date.split('/')
        folders = ['data', 'eth', year, month, day]
        path_so_far = ''
        for folder in folders:
            path_so_far = os.path.join(path_so_far, folder)
            if not os.path.exists(path_so_far):
                os.makedirs(path_so_far)
    
if __name__ == '__main__':
    opt_parser = OptionParser()
    opt_parser.add_option('-d',
                         '--date',
                         dest='date',
                         help='Specific date (YYYY/mm/dd) to collect data for, default to today, local time')
    opt_parser.add_option('-s',
                          '--start_date',
                          dest='start_date',
                          help='Start date if want to collect for more than one day')
    opt_parser.add_option('-e',
                          '--end_date',
                          dest='end_date',
                          help='End date, inclusive, if want to collect for more than one day')
    opt_parser.add_option('-i',
                          '--sampling_interval',
                          dest='sampling_interval',
                          help='Option to set sampling interval in minutes')
    (options, args) = opt_parser.parse_args()
    
    print("options: {0}".format(options))
    print("args: {0}".format(args))
    
    collect_data_obj = CollectData(date=options.date,
                                   start_date=options.start_date,
                                   end_date=options.end_date,
                                   sampling_interval = options.sampling_interval)
    collect_data_obj.run()
    

