import os


directory = "../samples/historical prices/"

for filename in os.listdir(directory):
    with open(directory+filename, 'r') as file:
        data = file.read()
        data = data.replace("\n\n", "\n").replace('{\n    "Note": "Thank you for using Alpha Vantage! Our standard API '
                                                  'call frequency is 5 calls per minute and 500 calls per day. Please '
                                                  'visit https://www.alphavantage.co/premium/ if you would like to '
                                                  'target a higher API call frequency."\n}', '')
        file.close()
    with open(directory+filename, 'w') as file:
        file.write(data)
        file.close()
