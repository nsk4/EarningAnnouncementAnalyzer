import requests
from datetime import date, timedelta
import time


page_link = 'https://finance.yahoo.com/calendar/earnings?size=100&day='
# 2019-01-30

d1 = date(2019, 1, 1)  # start date
d2 = date(2020, 4, 30)  # end date
delta = d2 - d1         # timedelta

max_request = 5
request_interval = 65


def extract_table(text):
    start_ind = text.find(
        '<table class="W(100%)"')
    start_ind = text.find('<tbody', start_ind)
    # Check if table exists and if it does not then return an empty string
    if start_ind == -1:
        return ""
    end_ind = text.find('</tbody>', start_ind + 1)
    return text[start_ind:end_ind + 8]


def extract_rows(text):
    str1 = '<td'
    str2 = '</td>'
    value = ''
    start = 0
    while True:
        new_row = ''
        for i in range(6):
            start_span_ind = text.find(str1, start)
            if start_span_ind == -1:
                return value

            start_ind = text.find('>', start_span_ind) + 1
            end_ind = text.find(str2, start_ind) + 1

            # First index is ticker which is wrapped into multiple tags
            if i == 0:
                start_ind = text.find('<a href=', start_ind)
                start_ind = text.find('>', start_ind) + 1

            # Last row is surprise which is wrapped into span
            if i== 2 or i == 5:
                start_ind = text.find('<span', start_ind)
                start_ind = text.find('>', start_ind) + 1

            # Skip starting react-text commend
            if text[start_ind:end_ind].startswith("<!--"):
                start_ind = start_ind = text.find('>', start_ind) + 1

            text_row = text[start_ind:end_ind]

            text_row = text_row.replace('<!-- /react-text -->', '')
            text_row = text_row.strip()
            text_row = text_row.replace('TAS', '-')
            text_row = text_row.replace('N/A', '-')
            text_row = text_row.replace('Before Market Open', 'bmo')
            text_row = text_row.replace('After Market Close', 'amo')
            text_row = text_row.replace('Time Not Supplied', '-')
            text_row = text_row.replace('"', '')
            text_row = text_row.replace('+', '')
            text_row = text_row[0:text_row.find("<")]

            if text_row == "":
                text_row = "-"

            if new_row != '':
                new_row = new_row + ','
            new_row = new_row + text_row
            start = end_ind
        value = value + new_row + '\n'

        print(new_row)


count = 0

for i in range(delta.days + 1):
    calculated_date = (d1 + timedelta(i))
    date_parameter = calculated_date.strftime('%Y-%m-%d')

    print(date_parameter)

    # Do 3 requests since each request can only capture 100 events at once
    page_response1 = requests.get(page_link + date_parameter + '&offset=0', timeout=60)
    table_data1 = extract_table(page_response1.text)

    page_response2 = requests.get(page_link + date_parameter + '&offset=100', timeout=60)
    table_data2 = extract_table(page_response2.text)

    page_response3 = requests.get(page_link + date_parameter + '&offset=200', timeout=60)
    table_data3 = extract_table(page_response3.text)

    text_file = open("new earning announcement data/" + calculated_date.strftime('%Y-%m-%d') + ".txt", "a+")
    text_file.write("ticker,company_name,consensus_eps_forecast,eps,surprise_percentage\n")
    text_file.write(extract_rows(table_data1))
    text_file.write(extract_rows(table_data2))
    text_file.write(extract_rows(table_data3))
    text_file.close()

    count = count + 1
    if count == max_request:
        count = 0
        print("Sleeping...")
        time.sleep(request_interval)




