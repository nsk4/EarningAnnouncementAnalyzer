import statistics

from dateutil import parser

import constants
import utilities


def get_dividend_jump(declaration_date, exdate, value, prices):
    all_market_dates = [*prices.keys()]
    if declaration_date in prices:
        date1 = declaration_date
    else:
        date1 = utilities.get_closest_previous_date(declaration_date, all_market_dates, 7)

    if exdate in prices:
        date2 = exdate
    else:
        date2 = utilities.get_closest_next_date(exdate, all_market_dates, 7)

    if date1 is None or date2 is None:
        return None

    return prices[date1][constants.CLOSE] - prices[date2][constants.OPEN] - float(value)


def dividend_data_to_feature_vectors(historical_prices, dividend_data):
    x_table = list()
    y_table = list()
    for ticker, dividends in dividend_data.items():
        # TODO: check if exdate is included in calcs

        # check if stock is not in s&p500
        if ticker not in historical_prices:
            continue
        print(ticker)

        prices = historical_prices[ticker]
        all_dates = [*dividends.keys()]
        for exdate, dividend in dividends.items():
            cash = dividend[0]
            declaration_date = dividend[1]
            proper_exdate = parser.parse(exdate)
            previous_dividend_date = utilities.get_previous_date(exdate, all_dates, 1)
            declaration_stock_date = utilities.get_closest_previous_date(declaration_date, [*prices.keys()])
            dividend_features = []
            dividend_result = 0

            if utilities.get_closest_next_date(exdate, [*prices.keys()], 7) is None or declaration_stock_date is None:
                # No point in keeping this record
                continue

            # price jump - before declaration and on exdate
            jump = get_dividend_jump(declaration_date, exdate, cash, prices)
            if jump is None:
                # No point in keeping this record
                continue
            if jump > 0:
                dividend_result = 1
            elif jump == 0:
                dividend_result = 0
            else:
                dividend_result = -1

            # 1. ticker_id
            dividend_features.append(ticker)

            # 2. dividend_yearly_yield
            # TODO: check if this make sense

            # 7. dividend_yield[0] > dividend_yield[-1 year]
            # TODO: check if this make sense

            # 3. dividend_yield[0]
            dividend_yield = cash / prices[declaration_stock_date][constants.CLOSE]
            dividend_features.append(dividend_yield)

            # 4. dividend_yield[-1]
            if previous_dividend_date is None:
                dividend_features.append(None)
            else:
                declaration_stock_date = utilities.get_closest_previous_date(previous_dividend_date, [*prices.keys()])
                if declaration_stock_date is None:
                    dividend_features.append(None)
                else:
                    previous_dividend_yield = cash / prices[declaration_stock_date][constants.CLOSE]
                    dividend_features.append(previous_dividend_yield)

            # 5. dividend_yield[-2]
            previous_previous_dividend_date = utilities.get_previous_date(exdate, all_dates, 2)
            if previous_previous_dividend_date is None:
                dividend_features.append(None)
            else:
                declaration_stock_date = utilities.get_closest_previous_date(previous_previous_dividend_date, [*prices.keys()])
                if declaration_stock_date is None:
                    dividend_features.append(None)
                else:
                    dividend_features.append(cash / prices[declaration_stock_date][constants.CLOSE])

            # 6. dividend_yield[0] > dividend_yield[-1]
            if previous_dividend_date is None:
                dividend_features.append(None)
            else:
                declaration_stock_date = utilities.get_closest_previous_date(previous_dividend_date, [*prices.keys()])
                if declaration_stock_date is None:
                    dividend_features.append(None)
                else:
                    previous_dividend_yield = cash / prices[declaration_stock_date][constants.CLOSE]
                    if dividend_yield > previous_dividend_yield:
                        dividend_features.append(1)
                    if dividend_yield == previous_dividend_yield:
                        dividend_features.append(0)
                    else:
                        dividend_features.append(-1)

            # 7. dividend_yield_previous_year
            # TODO: this

            # 8. Day
            dividend_features.append(proper_exdate.day)

            # 9. Month
            dividend_features.append(proper_exdate.month)

            # 10. Year
            dividend_features.append(proper_exdate.year)

            # 11. no of dividends in last year

            # 12. average volume between declaration and exdate
            calc = utilities.data_for_calc_between_dates(declaration_date, exdate, historical_prices[ticker], constants.VOLUME)
            if calc is None or len(calc) < 2:
                dividend_features.append(None)
            else:
                dividend_features.append(statistics.mean(calc))

            # 13. Standard deviation((High - Low) / close) / Mean((High - Low) / close) between declaration and exdate
            calc = utilities.price_calc_between_dates(declaration_date, exdate, historical_prices[ticker])
            if calc is None or len(calc) < 2:
                dividend_features.append(None)
            else:
                dividend_features.append(statistics.stdev(calc) / statistics.mean(calc))

            # 14. Standard deviation((High - Low) / close) between declaration and exdate.
            calc = utilities.price_calc_between_dates(declaration_date, exdate, historical_prices[ticker])
            if calc is None or len(calc) < 2:
                dividend_features.append(None)
            else:
                dividend_features.append(statistics.stdev(calc))

            x_table.append(dividend_features)
            y_table.append([dividend_result])
    return x_table, y_table
