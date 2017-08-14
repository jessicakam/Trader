# 2017/08/06
import gdax
import csv
from datetime import datetime, timedelta
from optparse import OptionParser
from os.path import join


class CollectData():
    
    SAMPLING_INTERVAL = 5
    INTERVAL_MULTIPLIER = 60
    DATE_FORMAT = '%Y/%m/%d'
    
    def __init__(self, **kwargs):
        self.public_client = gdax.PublicClient()
        today = datetime.utcnow()
        self.conversion_interested_in = 'ETH-USD'
        
        self.start_date = (today - timedelta(days=1)).strftime(CollectData.DATE_FORMAT)
        self.end_date = today.strftime(CollectData.DATE_FORMAT)
        if kwargs.get('date'):           
            self.start_date = (datetime.strptime(kwargs.get('date'), CollectData.DATE_FORMAT) - timedelta(days=1)).strftime(CollectData.DATE_FORMAT)    
            self.end_date = kwargs.get('date')
        if kwargs.get('start_date') and kwargs.get('end_date'):
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
        
        self.sampling_interval = CollectData.SAMPLING_INTERVAL * CollectData.INTERVAL_MULTIPLIER
        if kwargs.get('sampling_interval'):
            self.sampling_interval = int(kwargs.get('sampling_interval')) * CollectData.INTERVAL_MULTIPLIER
    
        #print(self.start_date)
        #print(self.end_date)
        #print(self.sampling_interval)
        
    def run(self):
        self.queryData()
        self.writeData()
        
    def queryData(self):
        start_str = self.isoString(self.start_date)
        end_str = self.isoString(self.end_date)
        self.data = self.public_client.get_product_historic_rates(self.conversion_interested_in, start=start_str, end=end_str, granularity=self.sampling_interval)
    
        #print(self.data)
    def writeData(self):
        output_file = self.generateFileName()
        print(output_file)
        csv_header = ['time', 'low', 'high', 'open', 'close', 'volume']
        with open(output_file, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(csv_header)
            for line in self.data:
                csv_writer.writerow(line)
                
    def isoString(self, date):
        date_obj = datetime.strptime(date, CollectData.DATE_FORMAT)
        #print(date_obj.isoformat())
        return date_obj.isoformat()
    
    def generateFileName(self):
        formatted_start_date = datetime.strptime(self.start_date, CollectData.DATE_FORMAT).strftime('%Y%m%d')
        return join('data',
                    'eth',
                    'gdax_data' + formatted_start_date + '.csv')
    
if __name__ == '__main__':
    opt_parser = OptionParser()
    opt_parser.add_option('-d',
                         '--date',
                         dest='date',
                         help='Specific date (YYYY/mm/dd) to collect data for')
    opt_parser.add_option('-s',
                          '--start_date',
                          dest='start_date',
                          help='Start date if want to collect for more than one day')
    opt_parser.add_option('-e',
                          '--end_date',
                          dest='end_date',
                          help='End date if want to collect for more than one day')
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
    

