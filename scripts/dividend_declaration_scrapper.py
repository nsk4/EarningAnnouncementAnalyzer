import requests
import time


page_link = 'https://www.nasdaq.com/symbol/'

max_request = 5
request_interval = 60

def get_query_url(symbol):
    return page_link + symbol + '/dividend-history'

def extract_table(text):
    start_ind = page_text.find('<table cellspacing="1" align="Center" rules="all" border="1" id="quotes_content_left_dividendhistoryGrid">')
    end_ind = page_text.find('</table>', start_ind + 1)
    return page_text[start_ind:end_ind + 8]

def extract_rows(text):
    str1 = '<span '
    str2 = '</span>'
    value = ''
    start = 0

    while True:
        new_row = ''
        for i in range(5):
            start_span_ind = text.find(str1, start)
            if start_span_ind == -1:
                return value
            start_ind = text.find('>', start_span_ind) + 1
            end_ind = text.find(str2, start_ind)
            if new_row != '':
                new_row = new_row + ','
            new_row = new_row + text[start_ind:end_ind]
            start = end_ind
        value = value + new_row + '\n'


with open("tickers.txt") as f:
    count = 0
    for symbol_unclean in f:
        symbol = symbol_unclean.replace("\n", "")

        print(symbol)

        page_response = requests.get(get_query_url(symbol), timeout=10)

        page_text = page_response.text
        table_data = extract_table(page_text)

        text_file = open("dividend declarations/"+symbol+".txt", "a+")
        text_file.write("exdate,cash_amount,declaration_date,record_date,payment_date\n")
        text_file.write(extract_rows(table_data))
        text_file.close()

        count = count + 1
        if count == max_request:
            count = 0
            print("Sleeping...")
            time.sleep(request_interval)

