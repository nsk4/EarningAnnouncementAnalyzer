import os


def get_data():
    historical_prices = {}
    directory = "samples/historical prices/"
    for filename in os.listdir(directory):
        ticker = filename.strip(".txt")
        historical_prices[ticker] = {}
        with open(directory + filename, "r") as ins:
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
    return historical_prices
