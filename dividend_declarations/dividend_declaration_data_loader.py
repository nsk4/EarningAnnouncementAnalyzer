import os
import csv
import constants
from dateutil import parser
from dividend_declarations import dividend_prediction


def get_data():
    dividend_data = {}
    directory = "samples/dividend declarations/"
    for filename in os.listdir(directory):
        ticker = filename.strip(".txt")
        with open(directory + filename, "r") as ins:
            next(ins)  # skip header row
            for line in ins:
                row_splits = line.strip('\n').split(',')
                if row_splits[constants.EXDATE] == "--" or row_splits[constants.DECLARATION_DATE] == "--":
                    continue

                if ticker not in dividend_data:
                    dividend_data[ticker] = {}
                exdate = (parser.parse(row_splits[constants.EXDATE])).strftime("%Y-%m-%d")
                declaration_date = (parser.parse(row_splits[constants.DECLARATION_DATE])).strftime("%Y-%m-%d")
                # if exdate == declaration_date:
                #    # This dividend is invalid for our analysis
                #    continue
                dividend_data[ticker][exdate] = (float(row_splits[constants.CASH_AMOUNT]), declaration_date)
    return dividend_data


def process_dividend_announcements(historical_prices, dividend_data, store_processed_data):
    x_table, y_table = dividend_prediction.dividend_data_to_feature_vectors(historical_prices, dividend_data)

    if store_processed_data:  # 5. store dividend data
        with open("models/x_data_dividend.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                               "f14", "f15", "f16"]])
            writer.writerows(x_table)

        with open("models/y_data_dividend.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["jump"]])
            writer.writerows(y_table)
    return x_table, y_table
