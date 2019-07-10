
names = ["BTC",	"ETH",	"XRP",	"LTC",	"REP",	"BCH",  "XMR",  "ETC"]

import pandas as pd
import requests
import dateutil.parser

#replace 552 in URL to number of days to retrieve start from your to_date"


def get_data(ticker,date):
    """ Query the API for X days historical price data starting from "date". """
    url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&limit=552&toTs={}".format(ticker,date)
    print(url)
    r = requests.get(url)
    ipdata = r.json()
    return ipdata

def get_df(tickers,from_date, to_date):
    """ Get historical price data between two dates. """
    date = to_date
    holder = []
    # While the earliest date returned is later than the earliest date requested, keep on querying the API
    # and adding the results to a list. 
    for ticker in tickers:
        data_raw = get_data(ticker,date)
        data_df = pd.DataFrame(data_raw['Data'])
        dts = pd.to_datetime(data_df['time'], unit='s') 
        cl  = data_df["close"]
        df = pd.DataFrame({"time": dts.values, ticker: cl.values})
        df = pd.DataFrame(cl.values, index=dts.values, columns=[ticker])
        #df.set_index('time', inplace=True)
        holder.append(df)    
    df_all = pd.concat(holder,axis=1)       
    return df_all

from_date = '06/01/2019'
to_date = '07/6/2019'
d_f = dateutil.parser.parse(from_date, dayfirst=False).timestamp()
d_t = dateutil.parser.parse(to_date, dayfirst=False).timestamp()
tickers = names
df = get_df(tickers, d_f, d_t)

df.to_csv(r'C:\xxxx/xxx\xxx/xxx.csv')
