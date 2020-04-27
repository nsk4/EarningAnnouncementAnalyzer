import csv
import json

from scripts.google_trend_extractor import extract_company_data
import dividend_prediction
import earning_prediction
import simulator
import machine_learning
from data_reader import read_data
import constants

from twitter import twitter_data_loader

if __name__ == "__main__":
    historical_prices = {}
    earning_announcement_times = {}
    earning_announcement_data = {}
    dividend_data = {}
    company_sentiment = {}
    trends = {}

    if constants.PROCESS_TWEETS:
        company_sentiment = twitter_data_loader.get_data(constants.USE_CACHED_TWEETS_DATA)

    if constants.PROCESS_GOOGLE_TRENDS:
        trends = extract_company_data()

    if constants.DO_BASIC_PROCESSING:
        historical_prices, earning_announcement_times, earning_announcement_data, dividend_data = read_data()
        print("Done reading data.")

        if constants.PROCESS_EARNING_ANNOUNCEMENTS:  # 2. feature vectors for earning announcements
            x_table, y_table = earning_prediction.earning_data_to_feature_vectors(historical_prices,
                                                                                  earning_announcement_times,
                                                                                  earning_announcement_data,
                                                                                  company_sentiment,
                                                                                  trends)

            if constants.STORE_DATA:  # 3. store earning announcement data
                with open("models/x_data_earning.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                                       "f14", "f15", "f16", "f17", "f18", "t1", "t2", "t3", "t4", "g1", "g2", "g3", "g4"]])
                    writer.writerows(x_table)

                with open("models/y_data_earning.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["jump"]])
                    writer.writerows(y_table)

        if constants.PROCESS_DIVIDEND_ANNOUNCEMENTS:  # 4. feature vectors for dividends
            x_table, y_table = dividend_prediction.dividend_data_to_feature_vectors(historical_prices, dividend_data)
            print(x_table, y_table)

            if constants.STORE_DATA:  # 5. store dividend data
                with open("models/x_data_dividend.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                                       "f14", "f15", "f16"]])
                    writer.writerows(x_table)

                with open("models/y_data_dividend.csv", "w", newline='') as my_csv:
                    writer = csv.writer(my_csv)
                    writer.writerows([["jump"]])
                    writer.writerows(y_table)

        if constants.RUN_SIMULATION:
            # result = simulator.run_simulation(historical_prices, earning_announcement_times, earning_announcement_data)
            # print("Final result:", result)
            trades = simulator.prepare_simulation_data(historical_prices, earning_announcement_times,
                                                       earning_announcement_data, company_sentiment, trends)
            with open("models/simulation_data.csv", "w", newline='') as my_csv:
                writer = csv.writer(my_csv)
                writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                                   "f14", "f15", "f16", "f17", "f18", "t1", "t2", "t3", "t4", "g1", "g2", "g3", "g4",
                                   "profit_buy", "profit_buy_percentage"]])
                writer.writerows(trades)

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
