# NOTE: this scrapper has become obsolete since EarningsCalendar changed their API and became subscription based

import requests
from datetime import date, timedelta
import time


page_link ='https://api.earningscalendar.net/earnings?&api_key=&date='

d1 = date(2019, 1, 1)  # start date
d2 = date(2019, 12, 31)  # end date
delta = d2 - d1         # timedelta

max_request = 5
request_interval = 65

text_file = open("earning_announcement_time_data.txt", "a+")
#text_file.write("timestamp,ticker,time\n")
text_file.close()

count = 0
for i in range(delta.days + 1):


    calculated_date = (d1 + timedelta(i))
    date_parameter = calculated_date.strftime('%Y%m%d')

    page_response = requests.get(page_link+date_parameter, timeout=60)

    for el in page_response.json():
        print(date_parameter, el['ticker'], el['when'])
        text_file = open("earning_announcement_time_data.txt", "a+")
        text_file.write(calculated_date.strftime('%Y-%m-%d') + "," + el['ticker'] + "," + el['when']+"\n")
        text_file.close()

    time.sleep(1)

    count = count + 1
    if count == max_request:
        count = 0
        print("Sleeping...")
        time.sleep(request_interval)
