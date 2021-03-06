# 2017/08/06
from optparse import OptionParser
from datetime import datetime, timedelta
from trader import ETHTrader

if __name__ == '__main__':
    opt_parser = OptionParser()
    today = datetime.utcnow()
    opt_parser.add_option('-d',
                         '--date',
                         dest='date',
                         help='Specific date (YYYY/mm/dd) to run trader on, default to yesterday')
    opt_parser.add_option('-s',
                          '--start_date',
                          dest='start_date',
                          help='Start date if want to run on more than one day')
    opt_parser.add_option('-e',
                          '--end_date',
                          dest='end_date',
                          help='End date if want to run on more than one day')
    opt_parser.add_option('-t',
                          '--train',
                          action='store_false',
                          dest='already_trained',
                          help='Use this option if initial model does not exist')
    opt_parser.add_option('-r',
                          '--retrain',
                          action='store_true',
                          dest='already_trained',
                          help='Use this option if want to retrain an existing model with new data')
    (options, args) = opt_parser.parse_args()

    trader = ETHTrader(date=options.date,
                       start_date=options.start_date,
                       end_date=options.end_date,
                       already_trained=options.already_trained)
    trader.run()