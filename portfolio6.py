# Import modules that will be used throughout the code
from alpha_vantage.timeseries import TimeSeries
import csv
import os
import sys

# Make sure users have the proper modules installed
print("Make sure you have: alpha_vantage, sys, csv, and os modules installed.")
# Create the function to display info about specific stocks
def display_detailed_stock_info(ticker, latest_prices, total_prices, stock_shares, previous_prices):
    try:
        # Create the variable for different data pieces
        detailed_stock_price = latest_prices[ticker]
        detailed_ticker_total_price = total_prices[ticker]
        number_of_shares = stock_shares.get(ticker, 1)
        previous_price = previous_prices.get(ticker, 0)
        detailed_stock_change = detailed_ticker_total_price - previous_price
        # Print the data pieces
        print(f"The stock is worth ${round(detailed_stock_price, 2)}")
        print(f"The total amount owned is ${round(detailed_ticker_total_price, 2)}")
        print(f"You own {number_of_shares} shares")
        print(f"Your net gain/loss for {ticker} today was: ${round(detailed_stock_change, 2)}")
    except KeyError:
        print(f"No data available for {ticker}.")

# A list of stocks in an example portfolio
stocks = ["ADBE", "BA", "DELL", "DIA", "DLTR", "LLY", "MSFT", "QQQ", "SPY", "TMUS", "YETI"]

try:
    # Replace "YOUR_API_KEY" with your actual API key
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not API_KEY:
        print("API key not found. Please set the ALPHA_VANTAGE_API_KEY environmental variable.")
        sys.exit()
    # Create the list to hold stock prices
    latest_prices = {}
    # Get the price for each stock in the list stocks
    for stock in stocks:
        data, _ = (TimeSeries(key=API_KEY, output_format='pandas')).get_quote_endpoint(stock)
        price = float(data["05. price"].iloc[0])
        latest_prices[stock] = price
        print(f"{stock}: ${price:.2f}")
except Exception as e:
    print(f"I'm sorry, but something has gone wrong while downloading stock prices. Perhaps double check your API key, or wait 5 minutes and try again: {e}")
    data = {}

# Calculate the total amount owned for each stock
stock_shares = {"DELL": 5, "SPY": 7, "TMUS": 2, "YETI": 8}
total_prices = {}
for stock in stocks:
    total_prices[stock] = latest_prices.get(stock, 0) * stock_shares.get(stock, 1)
# Calculate the total portfolio value
portfolio_value = sum(total_prices.values())

# Retreive the previous portfolio's value
if not os.path.exists("portfolio.csv"):
    previous_portfolio_value = 0
else:
    # Create an empty dictionary to assign a stock and it's value
    previous_prices = {}
    # Get the data from portfolio.csv
    with open("portfolio.csv", mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        if not rows:
            print("The data file is empty. Starting all portfolio valules fresh.")
            previous_prices, previous_portfolio_value = {}, 0
        else:
            header, *data = rows
            # Assign the previous portfolio value
            if header[0] == "portfolio value":
                previous_portfolio_value = float(header[1])
            # Assign the value for previous stocks
            for row in data:
                stock, price = row
                previous_prices[stock] = float(price)

# Calculate the net gain or loss
print(f"Your net gain/loss today was: ${round(portfolio_value - previous_portfolio_value, 2)}")

# Find out if the user wants to look at a specific stock in more detail
detailed_look = input("Would you like a more detailed look into any of your stocks? ")
if detailed_look in ["y", "Y", "yes", "Yes"]:
    # Determines the stock they would like to look at
    detailed_ticker = input("Which stock would you like to look at? (Remember to put the ticker in all caps). ")
    # Make sure the detailed ticker data is available
    if detailed_ticker not in stocks:
        print(f"{detailed_ticker} is not in your portfolio.")
    else:
        display_detailed_stock_info(detailed_ticker, latest_prices, total_prices, stock_shares, previous_prices)

# Record the current day's price per stock and portfolio value
try:
    with open("portfolio.csv", mode="w", newline="") as file2:
        writer = csv.writer(file2)
        writer.writerow(["portfolio value", portfolio_value])
        for stock, price in latest_prices.items():
            writer.writerow([stock, price])
except Exception as e:
    print(f"There was a problem saving the prices in portfolio.csv: {e}")
