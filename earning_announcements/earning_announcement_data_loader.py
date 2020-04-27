import os
import csv
from earning_announcements import earning_prediction
from time import strptime


def get_data(load_cached):
    if load_cached:
        return read_old_data()
        #old_data = merge_old_data(read_old_data())
        #new_data = read_new_data()
        ## TODO: merge these two together
    else:
        # TODO: read from file
        pass


def process_earning_announcements(historical_prices,
                                  earning_announcement_times,
                                  earning_announcement_data,
                                  company_sentiment,
                                  trends,
                                  store_processed_data):
    x_table, y_table = earning_prediction.earning_data_to_feature_vectors(historical_prices,
                                                                          earning_announcement_times,
                                                                          earning_announcement_data,
                                                                          company_sentiment,
                                                                          trends)

    if store_processed_data:  # 3. store earning announcement data
        with open("models/x_data_earning.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                               "f14", "f15", "f16", "f17", "f18", "t1", "t2", "t3", "t4", "g1", "g2", "g3", "g4"]])
            writer.writerows(x_table)

        with open("models/y_data_earning.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["jump"]])
            writer.writerows(y_table)

    return x_table, y_table


def read_old_data():
    # Earning announcement times (old times)
    earning_announcement_times = {}
    with open("samples/earning_announcement_time_data.txt", "r") as ins:
        next(ins)  # skip header row
        for line in ins:
            row_splits = line.strip('\n').split(',')
            if row_splits[1] not in earning_announcement_times:
                earning_announcement_times[row_splits[1]] = {}
            earning_announcement_times[row_splits[1]][row_splits[0]] = row_splits[2]

    # Earning announcement data (old data)
    earning_announcement_data = {}
    directory = "samples/earning announcement data/"
    for filename in os.listdir(directory):
        date = filename.strip(".txt")
        with open(directory + filename, "r") as ins:
            next(ins)  # skip header row
            for line in ins:
                if line == "company_name,market_cap,reported_date,fiscal_quarter_ending,consensus_eps_forecast," \
                           "num_of_ests,eps,surprise_percentage\n":
                    break
                row_splits = line.strip('\n').split(',')
                ticker = row_splits[0][row_splits[0].find('(') + 1:row_splits[0].find(')')]
                name = row_splits[0][:row_splits[0].find('(')]
                fiscal_year_end = strptime(row_splits[3][:3], '%b').tm_mon  # NOTE: changed from original research paper
                num_est = row_splits[5]

                # market cap
                if row_splits[1].lower() == "n/a":
                    market_cap = None
                elif row_splits[1][-1] == 'M':
                    market_cap = float(row_splits[1][1:-1]) * 1000000
                else:
                    market_cap = float(row_splits[1][1:-1]) * 1000000000

                # estimated eps
                if row_splits[4].lower() == "$n/a":
                    est_eps = None
                else:
                    est_eps = float(row_splits[4][1:])

                # eps
                if row_splits[6].lower() == "n/a":
                    eps = None
                else:
                    eps = float(row_splits[6][1:])

                # surprise percentage
                if row_splits[7].lower() == "n/a":
                    surprise_percentage = None
                elif row_splits[7].lower() == "met":
                    surprise_percentage = 0
                else:
                    surprise_percentage = float(row_splits[7])

                if ticker not in earning_announcement_data:
                    earning_announcement_data[ticker] = {}
                earning_announcement_data[ticker][date] = (name,
                                                           fiscal_year_end,
                                                           market_cap,
                                                           est_eps,
                                                           num_est,
                                                           eps,
                                                           surprise_percentage)
    return earning_announcement_times, earning_announcement_data

def merge_old_data(earning_announcement_times, earning_announcement_data):
    # TODO: merge these two together
    return None

def read_new_data():
    earning_announcement_data = {}
    directory = "samples/new earning announcement data/"
    for filename in os.listdir(directory):
        date = filename.strip(".txt")
        with open(directory + filename, "r") as ins:
            next(ins)  # skip header row
            for line in ins:
                if line.startswith("ticker,company_name"):
                    break
                row_splits = line.strip('\n').split(',')

                ticker = row_splits[0]
                time = row_splits[2]

                # estimated eps
                if row_splits[3] == "-":
                    est_eps = None
                else:
                    est_eps = float(row_splits[3])

                # eps
                if row_splits[5] == "-":
                    eps = None
                else:
                    eps = float(row_splits[5])

                # surprise percentage
                if row_splits[6] == "-":
                    surprise_percentage = 0
                else:
                    surprise_percentage = float(row_splits[6])

                if ticker not in earning_announcement_data:
                    earning_announcement_data[ticker] = {}
                earning_announcement_data[ticker][date] = (ticker, date, time, est_eps, eps, surprise_percentage)
    return earning_announcement_data
