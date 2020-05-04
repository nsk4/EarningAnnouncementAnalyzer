import csv

import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import constants
import utilities
from earning_announcements import earning_prediction


def get_data(historical_prices, earning_announcement_data, company_sentiment, trends, store_processed_data):
    print("Processing ML data")
    x_table, y_table, trades = do_all_processing(historical_prices,
                                                 earning_announcement_data,
                                                 company_sentiment,
                                                 trends)
    encoded_x = do_encoding(x_table)

    if store_processed_data:
        with open("models/ml_x.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13",
                               "f14", "f15", "f16", "f17", "f18", "t1", "t2", "t3", "t4", "g1", "g2", "g3",
                               "g4"]])
            writer.writerows(x_table)
        with open("models/ml_y.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["jump"]])
            writer.writerows(y_table)
        with open("models/ml_trade.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows([["profit_buy", "profit_buy_percentage"]])
            writer.writerows(trades)
        with open("models/ml_x_encoded.csv", "w", newline='') as my_csv:
            writer = csv.writer(my_csv)
            writer.writerows(encoded_x)

    return encoded_x, x_table, y_table, trades


def do_encoding(x_data):
    # 1) Define data encoding - OneHotEncoder
    if constants.VERBOSE:
        print("Defining categories")
    binary = [0, 1]
    triary = [-1, 0, 1]
    days = list(range(1, 32))
    months = list(range(1, 13))
    years = list(range(2014, 2020))

    # Encode X values
    encoded_x = []
    for i in range(len(x_data)):
        # if i > 1000: continue
        # print(x_data, end='\n')
        bin_1 = x_data[i][:4]
        num_1 = x_data[i][4:6]
        bin_2 = x_data[i][6]
        num_2 = x_data[i][7]
        # mix_1 = x_data[i][8:14]
        mix_1 = x_data[i][8:13]
        num_3 = x_data[i][14]
        mix_2 = x_data[i][15:18]
        num_4 = x_data[i][18:26]

        encoded_x.append(list(
            preprocessing.OneHotEncoder(handle_unknown='ignore',
                                        categories=[binary, binary, binary, binary]).fit_transform(
                [bin_1]).toarray()[
                0]) + list(num_1) +
                         list(preprocessing.OneHotEncoder(handle_unknown='ignore', categories=[binary]).fit_transform(
                             [[bin_2]]).toarray()[
                                  0]) + list([num_2]) +
                         list(preprocessing.OneHotEncoder(
                             # categories=[binary, binary, days, months, years, all_tickers]).fit_transform(
                             handle_unknown='ignore', categories=[binary, binary, days, months, years]).fit_transform(
                             [mix_1]).toarray()[0]) + list([num_3]) +
                         list(
                             preprocessing.OneHotEncoder(
                                 handle_unknown='ignore',
                                 categories=[triary, triary, constants.DISCRETE_JUMPS]).fit_transform(
                                 [mix_2]).toarray()[0]) + list(num_4))
    return encoded_x


def to_int_or_none(val):
    if val is None or val == "":
        return None
    else:
        return int(val)


def to_float_or_none(val):
    if val is None or val == "":
        return None
    else:
        return float(val)


def get_cached_data():
    print("Getting cached ML data")
    with open('models/ml_x.csv', 'r') as my_csv:
        next(my_csv, None)  # skip the headers
        x_table = [[to_int_or_none(row[0]), to_int_or_none(row[1]), to_int_or_none(row[2]), to_int_or_none(row[3]),
                    to_float_or_none(row[4]), to_float_or_none(row[5]),
                    to_int_or_none(row[6]), to_float_or_none(row[7]), to_int_or_none(row[8]), to_int_or_none(row[9]),
                    to_int_or_none(row[10]), to_int_or_none(row[11]),
                    to_int_or_none(row[12]), row[13], to_float_or_none(row[14]), to_int_or_none(row[15]),
                    to_int_or_none(row[16]), to_float_or_none(row[17]),
                    to_int_or_none(row[18]), to_int_or_none(row[19]), to_int_or_none(row[20]), to_int_or_none(row[21]),
                    to_float_or_none(row[22]), to_float_or_none(row[23]),
                    to_float_or_none(row[24]), to_float_or_none(row[25])] for row in csv.reader(my_csv, delimiter=',')]
    with open('models/ml_y.csv', 'r') as my_csv:
        next(my_csv, None)  # skip the headers
        y_table = [[int(row[0])] for row in csv.reader(my_csv, delimiter=',')]
    with open('models/ml_trade.csv', 'r') as my_csv:
        next(my_csv, None)  # skip the headers
        trades = [[float(row[0]), float(row[1])] for row in csv.reader(my_csv, delimiter=',')]
    with open('models/ml_x_encoded.csv', 'r') as data:
        reader = csv.reader(data)
        encoded_x = []
        for row in reader:
            encoded_x.append([float(i) for i in row])
    return encoded_x, x_table, y_table, trades


def run_machine_learning(encoded_x, x_data, y_data, trades, simulation_year):
    # 2) Create model from data
    if constants.VERBOSE:
        print("Creating model")
    X_table = list()
    Y_table = list()

    for i in range(len(x_data)):
        # if i > 1000: continue
        if x_data[i][constants.YEAR_FEATURE] != simulation_year:
            X_table.append(encoded_x[i])  # append encoded values, not the original ones
            Y_table.append(y_data[i][0])

    clf = LogisticRegression(random_state=None, solver='liblinear', penalty='l1', C=10, multi_class='ovr').fit(
        np.asarray(X_table),
        np.asarray(Y_table))

    # 3) Run analysis of trades
    if constants.VERBOSE:
        print("Running analysis")
    income = 0
    income_percentage = 0
    prediction_results = []
    real_results = []

    always_sell = 0
    always_sell_percentage = 0
    always_buy = 0
    always_buy_percentage = 0
    discrete_trades = [0] * len(constants.DISCRETE_JUMPS)
    discrete_won_trades = [0] * len(constants.DISCRETE_JUMPS)
    for i in range(len(x_data)):
        # if i > 1000: continue
        if x_data[i][constants.YEAR_FEATURE] != simulation_year:
            continue

        res_array = clf.predict_proba(np.asarray([encoded_x[i]]))[0]
        res_value = clf.predict(np.asarray([encoded_x[i]]))[0]

        if constants.CLASSIFY_RESULTS:
            if constants.CERTAINTY_BASED_TRADES:
                action = np.sign(constants.DISCRETE_JUMPS[res_value])
                coef = np.abs(
                    constants.DISCRETE_JUMPS[res_value])  # Multiply by 10 to ensure that numbers are not too small
            else:
                coef = 1
                if constants.DISCRETE_JUMPS[res_value] > 0:
                    action = constants.ORDER_BUY
                elif constants.DISCRETE_JUMPS[res_value] < 0:
                    action = constants.ORDER_SELL
                else:
                    action = constants.ORDER_NONE
        else:
            if constants.PREDICTION_THRESHOLD != 0:
                # If highest class is for at least threshold better than other classes then select it otherwise dont perform trade
                if res_array[1] > res_array[0] and res_array[1] > res_array[2]:
                    action = constants.ORDER_NONE
                elif abs(res_array[0] - res_array[2]) > constants.PREDICTION_THRESHOLD:
                    if res_array[0] > res_array[2]:
                        action = constants.ORDER_SELL
                    else:
                        action = constants.ORDER_BUY
                else:
                    action = constants.ORDER_NONE
            else:
                # use result
                action = res_value

            if constants.CERTAINTY_BASED_TRADES:
                coef = max(res_array) * 10  # Multiply by 10 to ensure that numbers are not too small
            else:
                # Do a full trade
                coef = 1

        income += action * trades[i][0] * coef
        trade_income_percentage = action * trades[i][1] * coef
        income_percentage += trade_income_percentage

        prediction_results.append(res_value)
        real_results.append(y_data[i][0])

        always_sell += -1 * trades[i][0]
        always_sell_percentage += -1 * trades[i][1]
        always_buy += trades[i][0]
        always_buy_percentage += trades[i][1]

        discrete_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] += 1
        if trade_income_percentage > 0:
            discrete_won_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] += 1
        elif trade_income_percentage < 0:
            discrete_won_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] -= 1

    if constants.VERBOSE:
        print("Done running")

    print("Year:", simulation_year, "Income:", round(income, 3),
          "Percentage (factor):", round(income_percentage, 3),
          "ML Score:", round(accuracy_score(np.asarray(real_results), np.asarray(prediction_results)), 3),
          "Always sell:", round(always_sell, 3),
          "Always sell percentage (factor):", round(always_sell_percentage, 3),
          "Always buy:", round(always_buy, 3),
          "Always buy percentage (factor):", round(always_buy_percentage, 3),
          "Total trades:", sum(discrete_trades),
          "Discrete trades count:", discrete_trades,
          "Trades ratio:", discrete_won_trades)

    if constants.VERBOSE:
        print("Predictions:", prediction_results)
        print("Real results:", real_results)
    return simulation_year, round(income, 3), round(income_percentage, 3)


def do_all_processing(historical_prices, earning_announcement_data, company_sentiment, trends):
    all_tickers = [*earning_announcement_data.keys()]
    x_data = []
    y_data = []
    trades = []

    for ticker in all_tickers:
        for date, announcements in earning_announcement_data[ticker].items():

            # TODO: try only BMO and AMC
            #print("Event " + ticker + " " + date + " " + announcements[constants.ANNOUNCEMENT_TIME])
            #if announcements[constants.ANNOUNCEMENT_TIME] != "bmo":
                #print("Event " + ticker + " " + date)
            #    continue
            #else:
            #    print("Event " + ticker + " " + date)

            if ticker not in historical_prices or \
                    utilities.get_closest_previous_date(date, [*historical_prices[ticker].keys()], 7) is None:
                continue

            # found an event for given date
            features = earning_prediction.extract_announcement_features(ticker,
                                                                        date,
                                                                        historical_prices[ticker],
                                                                        earning_announcement_data[ticker],
                                                                        company_sentiment,
                                                                        trends)
            if features is None:
                continue
            result = earning_prediction.extract_announcement_result(date,
                                                                    historical_prices[ticker],
                                                                    announcements[constants.ANNOUNCEMENT_TIME])

            after_date = utilities.get_after_announcement_date(date, historical_prices[ticker],
                                                               announcements[constants.ANNOUNCEMENT_TIME])
            profit_buy = historical_prices[ticker][after_date][constants.CLOSE] - historical_prices[ticker][after_date][
                constants.OPEN]
            profit_buy_percentage = profit_buy / historical_prices[ticker][after_date][constants.OPEN]

            x_data.append(features)
            y_data.append([result])
            trades.append([profit_buy, profit_buy_percentage])

    return x_data, y_data, trades
