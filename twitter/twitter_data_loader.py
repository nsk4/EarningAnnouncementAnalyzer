import json
from twitter import twitter_analysis
import constants

def get_data(load_cached):
    company_sentiment = {}
    if load_cached:
        with open('models/twitter_sentiment.json') as handle:
            company_sentiment = json.loads(handle.read())
    else:
        with open("samples/tickers.txt", "r") as ins:
            for line in ins:
                ticker = str.lower(line).replace("\n", "")
                if ticker is "":
                    continue
                company_sentiment[ticker] = {}
        company_sentiment["general_date_sentiment"] = {}  # general sentiment
        company_sentiment = twitter_analysis.get_twitter_sentiment(company_sentiment)
        if constants.STORE_DATA:
            with open('models/twitter_sentiment.json', 'w') as json_file:
                json.dump(company_sentiment, json_file)
    return company_sentiment
