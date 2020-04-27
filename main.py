import csv
from earning_announcements import earning_announcement_data_loader
from dividend_declarations import dividend_declaration_data_loader
from historical_prices import historical_prices_data_loader
from google_trends import google_trends_data_loader
import simulator
import machine_learning
import constants

from twitter import twitter_data_loader

if __name__ == "__main__":
    historical_prices = {}
    earning_announcement_times = {}
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
        historical_prices = historical_prices_data_loader.get_data(constants.USE_CACHED_HISTORICAL_PRICES)

    if constants.PROCESS_DIVIDEND_ANNOUNCEMENTS:
        dividend_data = dividend_declaration_data_loader.get_data(constants.USE_CACHED_DIVIDEND_DATA)
        x_table, y_table = dividend_declaration_data_loader.process_dividend_announcements(historical_prices,
                                                                                           dividend_data,
                                                                                           constants.STORE_DATA)

    if constants.PROCESS_EARNING_ANNOUNCEMENTS:
        earning_announcement_times, earning_announcement_data = earning_announcement_data_loader.get_data(constants.USE_CACHED_EARNING_ANNOUNCEMENTS)
        x_table, y_table = earning_announcement_data_loader.process_earning_announcements(historical_prices,
                                                                                          earning_announcement_times,
                                                                                          earning_announcement_data,
                                                                                          company_sentiment,
                                                                                          trends,
                                                                                          constants.STORE_DATA)

    if constants.RUN_SIMULATION:
        simulator.run_simulation(historical_prices, earning_announcement_times, earning_announcement_data, company_sentiment, trends)

    if constants.RUN_MACHINE_LEARNING:
        if constants.READ_DATA:
            with open('models/ml_x.csv', 'r') as my_csv:
                next(my_csv, None)  # skip the headers
                x_table = [[int(row[0]), int(row[1]), int(row[2]), int(row[3]), float(row[4]), float(row[5]),
                            int(row[6]), float(row[7]), int(row[8]), int(row[9]), int(row[10]), int(row[11]),
                            int(row[12]), row[13], float(row[14]), int(row[15]), int(row[16]), float(row[17]),
                            int(row[18]), int(row[19]), int(row[20]), int(row[21]), float(row[22]), float(row[23]),
                            float(row[24]), float(row[25])] for row in csv.reader(my_csv, delimiter=',')]
            with open('models/ml_y.csv', 'r') as my_csv:
                next(my_csv, None)  # skip the headers
                y_table = [[int(row[0])] for row in csv.reader(my_csv, delimiter=',')]
            with open('models/ml_trade.csv', 'r') as my_csv:
                next(my_csv, None)  # skip the headers
                trades = [[float(row[0]), float(row[1])] for row in csv.reader(my_csv, delimiter=',')]
        else:
            x_table, y_table, trades = simulator.do_all_processing(historical_prices,
                                                                   earning_announcement_times,
                                                                   earning_announcement_data,
                                                                   company_sentiment,
                                                                   trends)
            if constants.STORE_DATA:
                with open("models/ml_x.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                                       "f14", "f15", "f16", "f17", "f18", "t1", "t2", "t3", "t4", "g1", "g2", "g3", "g4"]])
                    writer.writerows(x_table)
                with open("models/ml_y.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["jump"]])
                    writer.writerows(y_table)
                with open("models/ml_trade.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["profit_buy", "profit_buy_percentage"]])
                    writer.writerows(trades)

        for i in range(2014, 2019):
            machine_learning.run_machine_learning(x_table, y_table, trades, i)
