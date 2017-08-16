# 2017/08/06
from optparse import OptionParser
from datetime import datetime, timedelta
from trader import RNNTrader

if __name__ == '__main__':
    opt_parser = OptionParser()
    today = datetime.utcnow()
    opt_parser.add_option('-d',
                         '--date',
                         dest='date',
                         help='Specific date (YYYY/mm/dd) to run trader on')
    opt_parser.add_option('-s',
                          '--start_date',
                          dest='start_date',
                          help='Start date if want to run on more than one day')
    opt_parser.add_option('-e',
                          '--end_date',
                          dest='end_date',
                          help='End date if want to run on more than one day')
    opt_parser.add_option('-a',
                          '--account_value',
                          dest='account_value',
                          help='Value of theoretical account')
    opt_parser.add_option('-E',
                          '--eth',
                          dest='eth',
                          help='Number of ETH in account')
    opt_parser.add_option('-B',
                          '--btc',
                          dest='btc',
                          help='Number of BTC in account')
    opt_parser.add_option('-l',
                          '--ltc',
                          dest='ltc',
                          help='Number of LTC in account')
    opt_parser.add_option('-i',
                          '--sample_interval',
                          dest='sample_interval',
                          help='Option to set sampling interval in minutes')
    (options, args) = opt_parser.parse_args()

    """
    Trader.run(date=options.date,
               start_date=options.start_date,
               end_date=options.end_date,
               account_value=options.account_value,
               eth=options.eth,
               btc=options.btc,
               ltc=options.ltc,
               sample_interval=options.sample_interval)
    """
    trader = RNNTrader()
    trader.importTrainingSet()
    trader.scaleFeatures()
    trader.getInputsAndOutputs()
    trader.reshape()
    trader.compileNN(optimizer='adam', loss='mean_squared_error')
    trader.fitToTrainingSet(batch_size = 32, epochs = 200)
    trader.makePredictions()
    trader.visualizeResults()
    trader.evaluate()
