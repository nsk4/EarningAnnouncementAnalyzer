import constants
import machine_learning
import simulator
from dividend_declarations import dividend_declaration_data_loader
from earning_announcements import earning_announcement_data_loader
from google_trends import google_trends_data_loader
from historical_prices import historical_prices_data_loader
from twitter import twitter_data_loader

if __name__ == "__main__":
    historical_prices = {}
    earning_announcement_data = {}
    dividend_data = {}
    company_sentiment = {}
    trends = {}
    earning_announcements = {}

    if constants.PROCESS_TWEETS:
        company_sentiment = twitter_data_loader.get_data(constants.USE_CACHED_TWEETS_DATA)

    if constants.PROCESS_GOOGLE_TRENDS:
        trends = google_trends_data_loader.get_data(constants.USE_CACHED_GOOGLE_TRENDS)

    if constants.PROCESS_HISTORICAL_PRICES:
        historical_prices = historical_prices_data_loader.get_data()

    if constants.PROCESS_DIVIDEND_ANNOUNCEMENTS:
        dividend_data = dividend_declaration_data_loader.get_data()
        x_table, y_table = dividend_declaration_data_loader.process_dividend_announcements(historical_prices,
                                                                                           dividend_data,
                                                                                           constants.STORE_DATA)

    if constants.PROCESS_EARNING_ANNOUNCEMENTS:
        earning_announcement_data = earning_announcement_data_loader.get_data()
        # x_table, y_table = earning_announcement_data_loader.process_earning_announcements(historical_prices,
        #                                                                                  earning_announcement_data,
        #                                                                                  company_sentiment,
        #                                                                                  trends,
        #                                                                                  constants.STORE_DATA)

    if constants.RUN_SIMULATION:
        simulator.run_simulation(historical_prices, earning_announcement_data, company_sentiment, trends)

    if constants.RUN_MACHINE_LEARNING:
        if constants.USE_CACHED_MACHINE_LEARNING_DATA:
            encoded_x, x_table, y_table, trades = machine_learning.get_cached_data()
        else:
            encoded_x, x_table, y_table, trades = machine_learning.get_data(historical_prices,
                                                                            earning_announcement_data,
                                                                            company_sentiment,
                                                                            trends,
                                                                            constants.STORE_DATA)
        final = list()
        for i in range(2014, 2019):
            res = machine_learning.run_machine_learning(encoded_x, x_table, y_table, trades, i)
            final.append(res)
        print(final)
