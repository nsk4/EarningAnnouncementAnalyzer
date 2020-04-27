import constants
import earning_prediction
import utilities


def do_all_processing(historical_prices, earning_announcement_times, earning_announcement_data, company_sentiment, trends):
    all_tickers = [*earning_announcement_data.keys()]
    x_data = []
    y_data = []
    trades = []

    for ticker in all_tickers:
        for date in earning_announcement_data[ticker]:

            if ticker not in historical_prices or \
                    ticker not in earning_announcement_times or \
                    ticker not in earning_announcement_data or \
                    date not in earning_announcement_data[ticker] or \
                    utilities.get_closest_previous_date(date, [*historical_prices[ticker].keys()], 7) is None:
                continue

            # found an event for given date
            features = earning_prediction.extract_announcement_features(ticker,
                                                                        date,
                                                                        historical_prices[ticker],
                                                                        earning_announcement_data[ticker],
                                                                        earning_announcement_times[ticker],
                                                                        company_sentiment,
                                                                        trends)
            if features is None:
                continue
            result = earning_prediction.extract_announcement_result(date,
                                                                    historical_prices[ticker],
                                                                    earning_announcement_times[ticker])

            after_date = utilities.get_after_announcement_dates(date, historical_prices[ticker],
                                                                earning_announcement_times[ticker])
            profit_buy = historical_prices[ticker][after_date][constants.CLOSE] - historical_prices[ticker][after_date][
                constants.OPEN]
            profit_buy_percentage = profit_buy / historical_prices[ticker][after_date][constants.OPEN]

            x_data.append(features)
            y_data.append([result])
            trades.append([profit_buy, profit_buy_percentage])

    return x_data, y_data, trades


def prepare_simulation_data(historical_prices, earning_announcement_times, earning_announcement_data, company_sentiment, trends):
    all_tickers = [*earning_announcement_data.keys()]
    trades = []

    start_date = constants.SIMULATOR_YEAR_START + "-01-01"
    end_date = constants.SIMULATOR_YEAR_END + "-01-01"
    date = start_date
    while date != end_date:
        print(date)
        # process earning announcements
        for ticker in all_tickers:
            if ticker not in historical_prices or \
                    ticker not in earning_announcement_times or \
                    ticker not in earning_announcement_data or \
                    date not in earning_announcement_data[ticker] or \
                    utilities.get_closest_previous_date(date, [*historical_prices[ticker].keys()], 7) is None:
                continue

            # found an event for given date
            features = earning_prediction.extract_announcement_features(ticker,
                                                                        date,
                                                                        historical_prices[ticker],
                                                                        earning_announcement_data[ticker],
                                                                        earning_announcement_times[ticker],
                                                                        company_sentiment,
                                                                        trends)

            after_date = utilities.get_after_announcement_dates(date, historical_prices[ticker],
                                                                earning_announcement_times[ticker])
            profit_buy = historical_prices[ticker][after_date][constants.CLOSE] - historical_prices[ticker][after_date][
                constants.OPEN]
            profit_buy_percentage = profit_buy / historical_prices[ticker][after_date][constants.OPEN]
            features.extend([profit_buy, profit_buy_percentage])
            trades.append(features)
        date = utilities.get_calendar_date(date, 1)
    return trades


def run_simulation(historical_prices, earning_announcement_times, earning_announcement_data, company_sentimentm, trends):
    all_tickers = [*earning_announcement_data.keys()]

    trade_queue = {}
    trade_log = []
    money = 0

    """
    on historical prices days do trading
    on announement times and data check announcement
    """
    start_date = "2014-01-01"
    end_date = "2019-05-31"
    date = start_date
    while date != end_date:
        # process earning announcements
        for ticker in all_tickers:
            if ticker not in historical_prices or \
                    ticker not in earning_announcement_times or \
                    ticker not in earning_announcement_data or \
                    date not in earning_announcement_data[ticker] or \
                    utilities.get_closest_previous_date(date, [*historical_prices[ticker].keys()], 7) is None:
                continue

            # found an event for given date
            features = earning_prediction.extract_announcement_features(ticker,
                                                                        date,
                                                                        historical_prices[ticker],
                                                                        earning_announcement_data[ticker],
                                                                        earning_announcement_times[ticker],
                                                                        company_sentimentm,
                                                                        trends)

            # TODO: run machine learning and get prediction
            result = features[16]

            after_date = utilities.get_after_announcement_dates(date, historical_prices[ticker],
                                                                earning_announcement_times[ticker])
            if result > 0:
                if after_date not in trade_queue:
                    trade_queue[after_date] = []
                trade_queue[after_date].append(tuple([ticker, constants.ORDER_BUY]))
            elif result < 0:
                if after_date not in trade_queue:
                    trade_queue[after_date] = []
                trade_queue[after_date].append(tuple([ticker, constants.ORDER_SELL]))

        # process trades
        if date in trade_queue:
            for ticker, order_type in trade_queue[date]:
                if order_type == constants.ORDER_NONE:
                    continue
                elif order_type == constants.ORDER_BUY:
                    jump = historical_prices[ticker][date][constants.CLOSE] - historical_prices[ticker][date][
                        constants.OPEN]
                elif order_type == constants.ORDER_SELL:
                    jump = historical_prices[ticker][date][constants.OPEN] - historical_prices[ticker][date][
                        constants.CLOSE]
                else:
                    print("RECORD ERROR IN TRADE QUEUE")
                    continue

                # TODO: scale by stock price
                # money += jump
                if jump > 0:
                    money += 1
                elif jump < 0:
                    money -= 1
                trade_log.append(tuple([date, ticker, order_type, jump]))
                # print("Traded:", (date, ticker, order_type, jump))

            # remove all trades
            trade_queue.pop(date, None)
            print("[", date, "]", "-", money)

        date = utilities.get_calendar_date(date, 1)

    return money
