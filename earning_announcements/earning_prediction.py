import statistics

from dateutil import parser

import constants
import utilities


def extract_announcement_features(ticker, date, prices, earning_announcements,
                                  earning_announcement_times, company_sentiment,
                                  trends):
    """
    Create announcement feature vector with given data
    :param ticker: Corporation ticker
    :param date: Announcement date
    :param prices: Corporation stock price history
    :param earning_announcements: Corporation earning announcements
    :param earning_announcement_times: Corporation earning announcements times
    :param company_sentiment: sentiment for all corporations
    :param trends: google trends
    :return: feature vector for given announcement event
    """

    all_dates = [*earning_announcements.keys()]
    announcement_features = []
    earning_announcement = earning_announcements[date]
    previous_announcement_date = utilities.get_previous_date(date, all_dates, 1)
    proper_date = parser.parse(date)

    # 1. Surprise factor[0] > 0
    if earning_announcement[constants.EPS] > 0:
        announcement_features.append(1)
    else:
        announcement_features.append(0)

    # 2. EPS[0] > EPS[-1].
    if previous_announcement_date is None:
        return None
        announcement_features.append(None)
    elif earning_announcement[constants.EPS] > earning_announcements[previous_announcement_date][constants.EPS]:
        announcement_features.append(1)
    else:
        announcement_features.append(0)

    # 3. EPS[-2] - 2 EPS[-1] + EPS[0] > 0.
    previous_previous_announcement_date = utilities.get_previous_date(date, all_dates, 2)
    if previous_announcement_date is None or previous_previous_announcement_date is None:
        return None
        announcement_features.append(None)
    elif earning_announcements[previous_previous_announcement_date][constants.EPS] \
            - 2 * earning_announcements[previous_announcement_date][constants.EPS] + \
            earning_announcement[constants.EPS] > 0:
        announcement_features.append(1)
    else:
        announcement_features.append(0)

    # 4. Earning Jump[-1] > 0.
    if previous_announcement_date is None:
        return None
        announcement_features.append(None)
    else:
        jump = utilities.get_announcement_jump(previous_announcement_date, prices,
                                               earning_announcement_times, constants.CLOSE, constants.OPEN)
        if jump is None:
            return None
            announcement_features.append(None)
        elif jump > 0:
            announcement_features.append(1)
        else:
            announcement_features.append(0)

    # 5. Standard deviation((High - Low) / close) / Mean((High - Low) / close) in last 90 days
    calc = utilities.price_calc(date, prices, 90)
    if calc is None:
        return None
        announcement_features.append(None)
    else:
        announcement_features.append(statistics.stdev(calc) / statistics.mean(calc))

    # 6. Standard deviation((High - Low) / close) / Mean((High - Low) / close) in last 10 days.
    calc = utilities.price_calc(date, prices, 10)
    if calc is None:
        return None
        announcement_features.append(None)
    else:
        announcement_features.append(statistics.stdev(calc) / statistics.mean(calc))

    # 7. 1 Billion < Market cap < 10 Billions.
    # NOTE: Market cap is not used since new data is not supporting it
    #if earning_announcement[constants.CAP] is None:
    #    return None
    #    announcement_features.append(None)
    #elif 1000000000 < earning_announcement[constants.CAP] < 10000000000:
    #    announcement_features.append(1)
    #else:
    #    announcement_features.append(0)
    announcement_features.append(0)

    # 8. Standard deviation((High - Low) / close) in last 90 days.
    calc = utilities.price_calc(date, prices, 90)
    if calc is None:
        return None
        announcement_features.append(None)
    else:
        announcement_features.append(statistics.stdev(calc))

    # 9. Earning Jump[-3] > 0.
    past_date = utilities.get_previous_date(date, all_dates, 3)
    if past_date is None:
        return None
        announcement_features.append(None)
    else:
        jump = utilities.get_announcement_jump(past_date, prices, earning_announcement_times,
                                               constants.CLOSE, constants.OPEN)
        if jump is None:
            return None
            announcement_features.append(None)
        elif jump > 0:
            announcement_features.append(1)
        else:
            announcement_features.append(0)

    # 10. Earning Jump[-2] > 0.
    past_date = utilities.get_previous_date(date, all_dates, 2)
    if past_date is None:
        return None
        announcement_features.append(None)
    else:
        jump = utilities.get_announcement_jump(past_date, prices, earning_announcement_times,
                                               constants.CLOSE, constants.OPEN)
        if jump is None:
            return None
            announcement_features.append(None)
        elif jump > 0:
            announcement_features.append(1)
        else:
            announcement_features.append(0)

    # 11. Day
    announcement_features.append(proper_date.day)

    # 12. Month
    announcement_features.append(proper_date.month)

    # 13. Year
    announcement_features.append(proper_date.year)

    # 14. ticker_id
    announcement_features.append(ticker)

    # 15. average volume in last 7 days
    announcement_features.append(statistics.mean(utilities.data_for_calc(date, prices, constants.VOLUME, 7)))

    # 16. EPS > EST EPS
    if earning_announcement[constants.EPS] is None or earning_announcement[constants.EST_EPS] is None:
        return None
        announcement_features.append(None)
    elif earning_announcement[constants.EPS] > earning_announcement[constants.EST_EPS]:
        announcement_features.append(1)
    elif earning_announcement[constants.EPS] == earning_announcement[constants.EST_EPS]:
        announcement_features.append(0)
    else:
        announcement_features.append(-1)

    # 17. earning jump
    jump = utilities.get_announcement_jump(date, prices, earning_announcement_times,
                                           constants.CLOSE, constants.OPEN, True)
    if jump is None:
        return None
        announcement_features.append(None)
    elif jump > constants.JUMP_THRESHOLD:
        announcement_features.append(1)
    elif jump < -constants.JUMP_THRESHOLD:
        announcement_features.append(-1)
    else:
        announcement_features.append(0)

    # 18. earning jump percentage discrete
    jump = utilities.get_announcement_jump(date, prices,
                                           earning_announcement_times,
                                           constants.CLOSE, constants.OPEN, True)
    if jump is None:
        return None
        announcement_features.append(None)
    else:
        announcement_features.append(utilities.get_discrete_jump(jump))
    """
    elif jump > threshold:
        announcement_features.append(1)
    elif jump < -threshold:
        announcement_features.append(-1)
    else:
        announcement_features.append(0)
    """

    if company_sentiment != {}:
        # 19. average positive-negative sentiment in the past month
        announcement_features.append(statistics.mean(utilities.get_avg_sentiment(company_sentiment["general_date_sentiment"], date, 30)))

        # 20. average positive-negative sentiment in the past week
        announcement_features.append(statistics.mean(utilities.get_avg_sentiment(company_sentiment["general_date_sentiment"], date, 7)))

        # 21. average positive-negative sentiment in the past month for company
        announcement_features.append(statistics.mean(utilities.get_avg_sentiment(company_sentiment[ticker], date, 30)))

        # 22. average positive-negative sentiment in the past week for company
        announcement_features.append(statistics.mean(utilities.get_avg_sentiment(company_sentiment[ticker], date, 7)))

    else:
        # TODO: temp workaround before we fill in twitter data
        announcement_features.append(0)
        announcement_features.append(0)
        announcement_features.append(0)
        announcement_features.append(0)

    if trends != {}:
        min_trend, max_trend, month_trend, week_trend = utilities.get_trend(trends[ticker], date)
        if min_trend is None or max_trend is None or month_trend is None or week_trend is None:
            return None

        # 24. trend in previous week
        announcement_features.append(week_trend)

        # 24. average trend in previous month
        announcement_features.append(month_trend)

        # 25. highest trend in previous month
        announcement_features.append(max_trend)

        # 25. lowest trend in previous month
        announcement_features.append(min_trend)
    else:
        announcement_features.append(0)
        announcement_features.append(0)
        announcement_features.append(0)
        announcement_features.append(0)

    date1, date2 = utilities.get_announcement_dates(date, prices, earning_announcement_times)
    date3 = utilities.get_after_announcement_dates(date, prices, earning_announcement_times)
    if date1 == date2 and date1 == date3 or date1 != date2 and date1 <= date3 < date2:
        raise Exception("Jump dates are similar. This should not happen!", date, date1, date2, date3)

    return announcement_features


def extract_announcement_result(date, prices, announcement_times):
    # after announcement jump result, if CLASSIFY_RESULTS is true then this function will return an index of appropriate discrete jumps array
    jump = utilities.get_after_announcement_jump(date, prices, announcement_times, True)
    if jump is None:
        return None
    elif constants.CLASSIFY_RESULTS:
        return utilities.get_discrete_jump_index(jump)
    elif jump > constants.EARNING_THRESHOLD:
        return 1
    elif jump < -constants.EARNING_THRESHOLD:
        return -1
    else:
        return 0


def earning_data_to_feature_vectors(historical_prices, earning_announcement_times,
                                    earning_announcement_data, company_sentiment,
                                    trends):
    x_table = list()
    y_table = list()
    for ticker, earning_announcements in earning_announcement_data.items():

        # check if stock is not in s&p500
        if ticker not in historical_prices or ticker not in earning_announcement_times:
            continue
        print(ticker)

        for date, earning_announcement in earning_announcements.items():

            announcement_result = extract_announcement_result(date,
                                                              historical_prices[ticker],
                                                              earning_announcement_times[ticker])
            if announcement_result is None:
                continue   # No point in keeping this record
            announcement_features = extract_announcement_features(ticker,
                                                                  date,
                                                                  historical_prices[ticker],
                                                                  earning_announcements,
                                                                  earning_announcement_times[ticker],
                                                                  company_sentiment,
                                                                  trends)
            if announcement_features is None:
                continue

            x_table.append(announcement_features)
            y_table.append([announcement_result])

    return x_table, y_table
