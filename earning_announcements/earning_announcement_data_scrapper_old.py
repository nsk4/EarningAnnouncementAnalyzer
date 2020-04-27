# NOTE: this scrapper has become obsolete since NASDAQ changed their formatting as well as migrating to one page application

import requests
from datetime import date, timedelta
import time

page_link = 'https://www.nasdaq.com/market-activity/earnings?date='
# 2016-Oct-28

d1 = date(2019, 1, 1)  # start date
d2 = date(2020, 3, 31)  # end date
delta = d2 - d1         # timedelta

max_request = 5
request_interval = 65


def extract_table(text):
    start_ind = text.find(
        '<table class="USMN_EarningsCalendar" id="ECCompaniesTable" border="0"cellpadding="0" cellspacing="0">')
    end_ind = text.find('</table>', start_ind + 1)
    return text[start_ind:end_ind + 8]

def extract_rows(text):
    str1 = '<td'
    str2 = '</td>'
    value = ''
    start = 0
    while True:
        new_row = ''
        for i in range(9):
            start_span_ind = text.find(str1, start)
            if start_span_ind == -1:
                return value
            start_ind = text.find('>', start_span_ind) + 1
            end_ind = text.find(str2, start_ind)

            text_row = text[start_ind:end_ind]
            if text_row.find('<td style="display:none">') >= 0:
                continue

            text_row = text_row.strip()
            text_row = text_row.replace(',', '')
            text_row = text_row.replace('</b></a>', '')
            text_row = text_row.replace('</span>', '')
            text_row = text_row.replace(' <br/><b>Market Cap: ', ',')
            tmp_ind = text_row.find('>')
            if tmp_ind >= 0:
                text_row = text_row[tmp_ind+1:len(text_row)]

            if new_row != '':
                new_row = new_row + ','
            new_row = new_row + text_row
            start = end_ind
        value = value + new_row + '\n'


count = 0

for i in range(delta.days + 1):
    calculated_date = (d1 + timedelta(i))
    date_parameter = calculated_date.strftime('%Y-%b-%d')

    print(date_parameter)

    page_response = requests.get(page_link + date_parameter, timeout=60)

    table_data = extract_table(page_response.text)

    text_file = open("earning announcement data/" + calculated_date.strftime('%Y-%m-%d') + ".txt", "a+")
    text_file.write("company_name,market_cap,reported_date,fiscal_quarter_ending,consensus_eps_forecast,num_of_ests,eps,surprise_percentage\n")
    text_file.write(extract_rows(table_data))
    text_file.close()

    count = count + 1
    if count == max_request:
        count = 0
        print("Sleeping...")
        time.sleep(request_interval)





