import datetime

from dateutil import parser
import statistics

import constants


def get_calendar_date(date, n):
    return (parser.parse(date) + datetime.timedelta(n)).strftime("%Y-%m-%d")


def get_closest_date(date, all_dates, max_diff=1):
    for i in range(max_diff + 1):
        new_date = get_calendar_date(date, -1 * i)
        if new_date in all_dates:
            return new_date

        new_date = get_calendar_date(date, i)
        if new_date in all_dates:
            return new_date
    return None


def get_closest_previous_date(date, all_dates, n=1):
    for i in range(n + 1):
        tmp_date = get_calendar_date(date, -1 * i)
        if tmp_date in all_dates:
            return tmp_date
    return None


def get_closest_next_date(date, all_dates, n=1):
    # get closest date to the given date. Can also be the same date
    for i in range(n + 1):
        tmp_date = get_calendar_date(date, i)
        if tmp_date in all_dates:
            return tmp_date
    return None


def get_previous_date(date, all_dates, n=1):
    date = get_closest_previous_date(date, all_dates, 7)
    if date is None:
        return None
    all_dates.sort()
    index = all_dates.index(date)
    for i in range(1, n + 1):
        if index - i < len(all_dates):
            return all_dates[index - i]
    return None


def get_next_date(date, all_dates, n=1):
    # get next date excluding current date
    date = get_closest_next_date(date, all_dates, 7)
    if date is None:
        return None
    all_dates.sort()
    index = all_dates.index(date)
    for i in range(1, n + 1):
        if index + i < len(all_dates):
            return all_dates[index + i]
    return None


def get_announcement_dates(date, prices, announcement_times):
    announcement_date = get_closest_date(date, [*announcement_times.keys()], 14)
    if announcement_date is None:  # if announcement was not found then assume --
        if date in [*prices.keys()]:
            return date, date
        previous_market_date = get_closest_previous_date(date, [*prices.keys()], 7)
        if previous_market_date is None:
            return None, None
        return previous_market_date, date

    if announcement_times[announcement_date] == "--" and date == announcement_date and date in prices:
        return date, date
    if announcement_times[announcement_date] == "bmo" or \
            announcement_times[announcement_date] == "--" and date < announcement_date:
        if announcement_date not in [*prices.keys()]:
            previous_market_date = get_closest_previous_date(announcement_date, [*prices.keys()], 7)
            announcement_date = get_closest_next_date(announcement_date, [*prices.keys()], 7)
        else:
            previous_market_date = get_previous_date(announcement_date, [*prices.keys()], 7)

        if previous_market_date is None or announcement_date is None:
            return None, None
        return previous_market_date, announcement_date
    elif announcement_times[announcement_date] == "amc" or \
            announcement_times[announcement_date] == "--" and announcement_date <= date:
        if announcement_date not in [*prices.keys()]:
            next_market_date = get_closest_next_date(announcement_date, [*prices.keys()], 7)
            announcement_date = get_closest_previous_date(announcement_date, [*prices.keys()], 7)
        else:

            next_market_date = get_next_date(announcement_date, [*prices.keys()], 7)

        if next_market_date is None or announcement_date is None:
            return None, None

        return announcement_date, next_market_date
    else:
        return None, None


def get_announcement_jump(date, prices, announcement_times, type1, type2, use_percentage=False):
    date1, date2 = get_announcement_dates(date, prices, announcement_times)
    if date1 is None or date2 is None:
        return None
    elif date1 == date2:
        jump = prices[date1][type1] - prices[date2][type2]
    else:
        jump = prices[date2][type2] - prices[date1][type1]

    if use_percentage is None or use_percentage is False:
        return jump
    else:
        return jump / prices[date1][type1]


def get_after_announcement_dates(date, prices, announcement_times):
    # BMO -> do trade next opening (same day)
    # AMC -> do trade next opening (next day)
    # -- and time is before event date -> assume BMO
    # -- and time is after event date -> assume AMC

    announcement_date = get_closest_date(date, [*announcement_times.keys()], 14)
    if announcement_date is None:  # if announcement was not found then assume --
        next_market_date = get_next_date(date, [*prices.keys()], 7)
        if next_market_date is None:
            return None
        return next_market_date
    elif announcement_times[announcement_date] == "bmo" or \
            announcement_times[announcement_date] == "--" and date < announcement_date:
        if announcement_date in [*prices.keys()]:
            return announcement_date
        return get_closest_next_date(announcement_date, [*prices.keys()], 7)
    elif announcement_times[announcement_date] == "amc" or \
            announcement_times[announcement_date] == "--" and announcement_date <= date:
        return get_next_date(announcement_date, [*prices.keys()], 7)
    else:
        return None


def get_after_announcement_jump(date, prices, announcement_times, use_percentage=False):
    announcement_date = get_after_announcement_dates(date, prices, announcement_times)
    if announcement_date is None:
        return None

    starting_date = get_closest_next_date(get_calendar_date(date, constants.JUMP_START), [*prices.keys()], 7)
    if starting_date is None:
        return None

    ending_date = get_closest_next_date(get_calendar_date(date, constants.JUMP_END), [*prices.keys()], 7)
    if ending_date is None:
        return None

    jump = prices[ending_date][constants.CLOSE] - prices[starting_date][constants.OPEN]
    if use_percentage is None or use_percentage is False:
        return jump
    else:
        return jump / prices[starting_date][constants.OPEN]


def price_calc(date, prices, n):
    keys = [*prices.keys()]
    keys.sort()

    date = get_closest_previous_date(date, keys, 7)
    if date is None:
        return None

    start_date_index = keys.index(date)
    data = []
    for i in range(1, n + 1):
        if start_date_index - i >= 0:
            day_price = prices[keys[start_date_index - i]]
            calc = (day_price[constants.HIGH] - day_price[constants.LOW]) / day_price[constants.CLOSE]
            data.append(calc)
        else:
            break
    return data


def price_calc_between_dates(date1, date2, prices):
    keys = [*prices.keys()]
    keys.sort()

    start_date = get_closest_next_date(date1, keys, 7)
    end_date = get_closest_previous_date(date2, keys, 7)
    if start_date is None or end_date is None:
        return None

    start_date_index = keys.index(start_date)
    end_date_index = keys.index(end_date)
    data = []
    for i in range(start_date_index, end_date_index+1):
        day_price = prices[keys[i]]
        calc = (day_price[constants.HIGH] - day_price[constants.LOW]) / day_price[constants.CLOSE]
        data.append(calc)
    return data


def data_for_calc(date, prices, data_type, n):
    keys = [*prices.keys()]
    keys.sort()

    date = get_closest_previous_date(date, keys, 7)
    if date is None:
        return None

    start_date_index = keys.index(date)
    data = []
    for i in range(1, n + 1):
        if start_date_index - i >= 0:
            data.append(prices[keys[start_date_index - i]][data_type])
        else:
            break
    return data


def data_for_calc_between_dates(date1, date2, prices, data_type):
    keys = [*prices.keys()]
    keys.sort()

    start_date = get_closest_next_date(date1, keys, 7)
    end_date = get_closest_previous_date(date2, keys, 7)
    if start_date is None or end_date is None:
        return None

    start_date_index = keys.index(start_date)
    end_date_index = keys.index(end_date)
    data = []
    for i in range(start_date_index, end_date_index+1):
        data.append(prices[keys[i]][data_type])
    return data


def get_closest_index(lst, K):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - K))


def get_closest_element(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def get_discrete_jump(jump):
    if jump is None:
        return None
    return get_closest_element(constants.DISCRETE_JUMPS, jump)


def get_discrete_jump_index(jump):
    if jump is None:
        return None
    return get_closest_index(constants.DISCRETE_JUMPS, jump)


def get_avg_sentiment(sentiment, date, n=7):
    sentiment_positive = [0] * n
    sentiment_negative = [0] * n

    for i in range(1, n+1):
        sentiment_date = get_calendar_date(date, -i)
        if sentiment_date in sentiment:
            sentiment_positive[-i] = sentiment[date]["positive"]
            sentiment_negative[-i] = sentiment[date]["negative"]

    sentiment_ratio = [x / y for x, y in zip(sentiment_positive, sentiment_negative)]
    return sentiment_ratio


def get_trend(company_trend, date):
    trend_dates = [*company_trend.keys()]

    last_trends = [0, 0, 0, 0]
    trend_date = date
    for i in range(1, 5):
        trend_date = get_previous_date(trend_date, trend_dates)
        if trend_date is None:
            last_trends[-i] = None
            break
        else:
            last_trends[-i] = company_trend[trend_date]

    week_trend = last_trends[-1]
    if week_trend is None:
        return None
    final_trend = []
    for val in last_trends:
        if val is not None:
            final_trend.append(val)

    print(final_trend)
    return min(final_trend), max(final_trend), statistics.mean(final_trend), week_trend
