import argparse
import requests
import json
import datetime

api_key = "U28PR4U6WSB1BIQN"
api_url_base = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=H24.F&apikey=U28PR4U6WSB1BIQN"

#get 

parser = argparse.ArgumentParser()
parser.add_argument("--date", help="enter a date (format: YYYY-MM-DD), which is in the week to be considered", type=str)
args = parser.parse_args()

if args.date:
    date_input = args.date
else:
    date_input = input("Please enter a date (Format: YYYY-MM-DD) :")

try:
    date_value = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
except ValueError:
    print("Wrong format! \nUsage: \"python stockquotes.py\" \nor \"python stockquotes.py --date YYYY-MM-DD\"")
    exit()

start_date = date_value - datetime.timedelta(date_value.weekday())


#request

def do_request():

    response = requests.get(api_url_base)

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None
    
response_data = do_request()

# store and analyse relevant data

symbol = response_data["Meta Data"]["2. Symbol"]
data = response_data["Time Series (Daily)"]

stock_quotes = {}

for key, value in data.items():
    d = datetime.datetime.strptime(key, "%Y-%m-%d").date()
    if d >= start_date and d <= (start_date + datetime.timedelta(days = 6)):
        stock_quotes[d] = value["4. close"]
    else:
        continue

#output

list_stock_quotes = ["/","/","/","/","/"]   
for key, value in stock_quotes.items():
    list_stock_quotes[key.weekday()] = value
    
stock_quotes_string = ""

for i in list_stock_quotes:
    stock_quotes_string += (i + "\t\t")

start_date_string = start_date.strftime("%b %d, %Y")
end_date_string = (start_date + datetime.timedelta(days = 4)).strftime("%b %d, %Y")

print("\nhome24 SE ("+symbol+")")
print("Frankfurt. Currency in EUR")
print("Time Period: " + start_date_string + " - " + end_date_string)
print("\nMo\t\tTu\t\tWe\t\tTh\t\tFr")
print(stock_quotes_string +"\n")

