import requests
import time


api_key = '6MLR97VET7AK68HC'
page_link = 'https://www.alphavantage.co/query'

# api_type = 'compact'
api_type = 'full'

max_request = 5
request_interval = 60

def get_api_query(symbol):
    return page_link+'?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize='+api_type+'&apikey='+api_key+'&datatype=csv'

with open("tickers.txt") as f:
    count = 0
    for symbol_unclean in f:
        symbol = symbol_unclean.replace("\n", "")

        print(symbol)

        page_response = requests.get(get_api_query(symbol), timeout=20)

        text_file = open("historical prices/"+symbol+".txt", "a+")
        text_file.write(page_response.text)
        text_file.close()

        count = count + 1
        if count == max_request:
            count = 0
            print("Sleeping...")
            time.sleep(request_interval)
