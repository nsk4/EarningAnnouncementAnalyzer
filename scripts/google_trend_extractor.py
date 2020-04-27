import os


def extract_company_data():
    trend_data = {}
    directory = "samples/trends/"
    for filename in os.listdir(directory):
        with open(directory + filename, "r") as ins:
            next(ins)  # skip category row
            next(ins)  # skip empty row

            ticker = ""
            for line in ins:
                if line.startswith("Week"):
                    ticker = line.split(',')[1].split(':')[0]
                    if ticker not in trend_data:
                        trend_data[ticker] = {}
                    continue

                row_splits = line.strip('\n').split(',')
                trend_data[ticker][row_splits[0]] = int(row_splits[1])
    return trend_data
