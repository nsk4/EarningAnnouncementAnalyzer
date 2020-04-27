# NOTE: this gets most detailed data, it is not feasible to download that much data via scrapper with all the delays build in

import time
from pytrends.request import TrendReq

def get_pytrends_data():
    with open("tickers.txt", "r") as ins:
        for ticker_raw in ins:
            ticker = ticker_raw.replace('\r', '').replace('\n', '')
            if len(ticker) < 2:
                print("Ticker to short:", ticker)
                continue
            for year in range(2015, 2019):
                print("Getting data for", ticker, "for year", year)
                df = TrendReq(hl='en-US', tz=360).get_historical_interest([ticker], year_start=year, month_start=1,
                                                                          day_start=1, hour_start=0, year_end=year,
                                                                          month_end=12, day_end=31, hour_end=23, cat=0,
                                                                          geo='', gprop='', sleep=10)
                #print(df)
                file = open("trends/" + ticker + "_" + str(year) + ".txt", "w", newline='')
                file.write(df.to_csv())
                file.close()

                time.sleep(120)
