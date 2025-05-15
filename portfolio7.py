# Import modules that will be used throughout the code
from alpha_vantage.timeseries import TimeSeries
import csv
import os
import sys

# Make sure users have the proper modules installed
print("Make sure you have: alpha_vantage, sys, csv, and os modules installed.")

# Create the function to display info about specific stocks, the variables in the () are the data pieces that will be used
def display_detailed_stock_info(ticker, latest_prices, total_prices, stock_shares, previous_prices):
    """Displays certain information about a specific stock"""
    try:
        # Create the variable for different data pieces
        # Get the total price(the amount times shares) for the stock
        detailed_stock_total_price = total_prices[ticker]
        # Get the previous price for the stock
        previous_price = previous_prices.get(ticker, 0)
        # Calculate the change in price
        detailed_stock_change = detailed_stock_total_price - previous_price
        # Print the data pieces
        print(f"The stock is worth ${round(latest_prices[ticker], 2)}")
        print(f"The total amount owned is ${round(detailed_stock_total_price, 2)}")
        print(f"You own {stock_shares.get(ticker, 1)} shares")
        print(f"Your net gain/loss for {ticker} today was: ${round(detailed_stock_change, 2)}")
    # Make sure that the program doesn't crash if the user enters a ticker that doesn't exist
    except KeyError:
        print(f"No data available for {ticker}.")

# A list of stocks in an example portfolio
stocks = ["ADBE", "BA", "DELL", "DIA", "DLTR", "LLY", "MSFT", "QQQ", "SPY", "TMUS", "YETI"]

# Retrieves the stock prices from the Alpha Vantage API
def get_stock_prices():
    """Obtains the latest closing price for each stock in the list"""
    try:
        # Make sure you export the API key as an environmental variable
        # Retrieve the API key from the environment variable
        API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
        # Quit the program if the API key is not found because nothing works without it
        if not API_KEY:
            print("API key not found. Please set the ALPHA_VANTAGE_API_KEY environmental variable.")
            sys.exit()
        # Create the list to hold stock prices
        latest_prices = {}
        # Get the price for each stock in the list stocks
        for stock in stocks:
            # Create a table to hold the data
            data, _ = (TimeSeries(key=API_KEY, output_format='pandas')).get_quote_endpoint(stock)
            # Takes the closing price for the specified stock
            price = float(data["05. price"].iloc[0])
            # Adds the price to the dictionary
            latest_prices[stock] = price
            # Tell the user the price of the stock
            print(f"{stock}: ${price:.2f}")
        # Return all the data
        return latest_prices
    # Make sure the program doesn't crash if the API fails or the API can't retrieve the data
    except Exception as e:
        print(f"I'm sorry, but something has gone wrong while downloading stock prices. Perhaps double check your API key, or wait 5 minutes and try again: {e}")
        data = {}

# Create the function to calculate the total amount owned for each stock
def get_stock_totals(latest_prices):
    """Calculates how much total money is invested in each stock"""
    # Specify the number of shares owned for each stock. If one share is owned, it will default to 1
    stock_shares = {"DELL": 5, "SPY": 7, "TMUS": 2, "YETI": 8}
    # Create an empty dictionary to assign a stock and it's value
    total_prices = {}
    for stock in stocks:
        # Find the total price by multiplying the individual price by the number of shares owned
        total_prices[stock] = latest_prices.get(stock, 0) * stock_shares.get(stock, 1)
    # Calculate the total portfolio value
    portfolio_value = sum(total_prices.values())
    # Return the values for future use
    return total_prices, portfolio_value, stock_shares

# Create the function to read the csv file and get previous data
def get_previous_prices():
    """Reads portfolio.csv and retrieves the prices of each stock and the prices of the portfolio from the time it was last run"""
    # Make sure the file exists before trying to read it
    if not os.path.exists("portfolio.csv"):
        # Return 0s if there is no data
        return {}, 0
    else:
        # Create an empty dictionary to assign a stock and it's value
        previous_prices = {}
        # Get the data from portfolio.csv
        with open("portfolio.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            # Return all 0s if there is no data
            if not rows:
                print("The data file is empty. Starting all portfolio values fresh.")
                return {}, 0
            # Assign the stocks and their values to the dictionary
            else:
                header, *data = rows
                # Assign the previous portfolio value
                if header[0] == "portfolio value":
                    previous_portfolio_value = float(header[1])
                # Assign the value for previous stocks
                for row in data:
                    # The stock is listed first, then a comma, then the price
                    stock, price = row
                    previous_prices[stock] = float(price)
                # Return the data for future use
                return previous_prices, previous_portfolio_value

# Create the function to display the portfolio value and ask if the user wants to look at a specific stock
def detailed_look(latest_prices, total_prices, stock_shares, previous_prices):
    """If the user wants it, the program will display detailed info about a specific stock"""
    # Find out if the user wants to look at a specific stock in more detail
    detailed_look = input("Would you like a more detailed look into any of your stocks? ")
    # Only continue if they say yes. If they say no, or anything else, exit the program
    if detailed_look in ["y", "Y", "yes", "Yes"]:
        # Use an infinite loop to make sure the user enters a valid ticker
        while True:
            # Determines the stock they would like to look at
            detailed_ticker = input("Which stock would you like to look at? (Remember to put the ticker in all caps). ")
            # Make sure the detailed ticker data is available
            if detailed_ticker not in stocks:
                print(f"{detailed_ticker} is not in your portfolio.")
            else:
                # Call the function to display the detailed stock info
                display_detailed_stock_info(detailed_ticker, latest_prices, total_prices, stock_shares, previous_prices)
                # Exit the infinite loop
                break
    else:
        # Save and leave if they don't want an individual price
        print("Thanks for using the program. Have a great day!")
        return

# Create a function to save the day's prices to the csv file to use the next day
def record_prices(latest_prices, portfolio_value):
    """Saves the price of each stock and the price of the portfolio to portfolio.csv to be used the next day"""
    try:
        # Open the file as file2, we already had file
        with open("portfolio.csv", mode="w", newline="") as file2:
            writer = csv.writer(file2)
            # Write the portfolio value first
            writer.writerow(["portfolio value", portfolio_value])
            # Then, write the stocks
            for stock, price in latest_prices.items():
                writer.writerow([stock, price])
    except Exception as e:
        print(f"There was a problem saving the prices in portfolio.csv: {e}")

# Create the main function to run the program
def main():
    """The main function that uses everything else to run the program"""
    # Get the various variables that will be used in other functions
    latest_prices = get_stock_prices()
    total_prices, portfolio_value, stock_shares = get_stock_totals(latest_prices)
    previous_prices, previous_portfolio_value = get_previous_prices()
    # Calculate the net gain or loss
    print(f"Your net gain/loss today was: ${round(portfolio_value - previous_portfolio_value, 2)}")
    # Call detailed_look()
    detailed_look(latest_prices, total_prices, stock_shares, previous_prices)
    # Record the prices to the csv file
    record_prices(latest_prices, portfolio_value)

# Run the program if called directly
if __name__ == "__main__":
    main()
