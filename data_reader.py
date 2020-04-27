import os
from time import strptime
from dateutil import parser

import constants


def read_data():
    # 1.1 price history
    historical_prices = {}
    directory = "samples/historical prices/"
    for filename in os.listdir(directory):
        ticker = filename.strip(".txt")
        historical_prices[ticker] = {}
        with open(directory+filename, "r") as ins:
            next(ins)  # skip header row
            for line in ins:
                if line == "timestamp,open,high,low,close,adjusted_close,volume,dividend_amount,split_coefficient\n":
                    break
                row_splits = line.strip('\n').split(',')
                if len(row_splits) < 6:
                    print("Error parsing", ticker)
                    continue
                historical_prices[ticker][row_splits[0]] = (float(row_splits[6]),
                                                            float(row_splits[2]),
                                                            float(row_splits[3]),
                                                            float(row_splits[1]),
                                                            float(row_splits[4]),
                                                            float(row_splits[5]))

    # 1.2 earning announcement times (old times)
    earning_announcement_times = {}
    with open("samples/earning_announcement_time_data.txt", "r") as ins:
        next(ins)  # skip header row
        for line in ins:
            row_splits = line.strip('\n').split(',')
            if row_splits[1] not in earning_announcement_times:
                earning_announcement_times[row_splits[1]] = {}
            earning_announcement_times[row_splits[1]][row_splits[0]] = row_splits[2]

    # 1.3 earning announcement data (old data)
    earning_announcement_data = {}
    directory = "samples/earning announcement data/"
    for filename in os.listdir(directory):
        date = filename.strip(".txt")
        with open(directory+filename, "r") as ins:
            next(ins)  # skip header row
            for line in ins:
                if line == "company_name,market_cap,reported_date,fiscal_quarter_ending,consensus_eps_forecast," \
                           "num_of_ests,eps,surprise_percentage\n":
                    break
                row_splits = line.strip('\n').split(',')
                ticker = row_splits[0][row_splits[0].find('(')+1:row_splits[0].find(')')]
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

    # 1.5 Merge old earning announcement times and data


    # 1.6 earning announcements (new data)
    new_earning_announcement_data = {}
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

                if ticker not in new_earning_announcement_data:
                    new_earning_announcement_data[ticker] = {}
                new_earning_announcement_data[ticker][date] = (ticker,
                                                               date,
                                                               time,
                                                               est_eps,
                                                               eps,
                                                               surprise_percentage)

    # 1.7 dividend data
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
                #if exdate == declaration_date:
                #    # This dividend is invalid for our analysis
                #    continue
                dividend_data[ticker][exdate] = (float(row_splits[constants.CASH_AMOUNT]), declaration_date)

    return historical_prices, earning_announcement_times, earning_announcement_data, dividend_data
