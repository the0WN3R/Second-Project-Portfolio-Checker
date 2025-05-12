from alpha_vantage.timeseries import TimeSeries
import sys

stocks = ["ADBE", "BA", "DELL", "DIA", "DLTR", "LLY", "MSFT", "QQQ", "SPY", "TMUS", "YETI"]

try:
    API_KEY = "YOUR_API_CODE"
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    latest_prices = {}
    for stock in stocks:
        try:
            data, _ = ts.get_quote_endpoint(stock)
            price = float(data["05. price"].iloc[0])
            latest_prices[stock] = price
            print(f"{stock}: ${round(price, 2)}")
        except Exception:
            print(f"I'm sorry, something has gone wrong while loading {stock}'s price.")
except Exception:
    print("I'm sorry, but something has gone wrong while downloading stock prices.")
    data = {}

ADBE_price = latest_prices.get("ADBE", 0)
BA_price = latest_prices.get("BA", 0)
DELL_price = latest_prices.get("DELL", 0) * 5
DIA_price = latest_prices.get("DIA", 0)
DLTR_price = latest_prices.get("DLTR", 0)
LLY_price = latest_prices.get("LLY", 0)
MSFT_price = latest_prices.get("MSFT", 0)
QQQ_price = latest_prices.get("QQQ", 0)
SPY_price = latest_prices.get("SPY", 0) * 7
TMUS_price = latest_prices.get("TMUS", 0) * 2
YETI_price = latest_prices.get("YETI", 0) * 8

portfolio_value = ADBE_price + BA_price + DELL_price + DIA_price + DLTR_price + LLY_price + MSFT_price + QQQ_price + SPY_price + TMUS_price + YETI_price

with open("portfolio.txt") as file:
    previous_portfolio_value = float(file.read().strip())

print(f"Your net gain/loss today was: ${round(portfolio_value - previous_portfolio_value, 2)}")

with open("portfolio.txt", "w") as file2:
    file2.write(str(portfolio_value))

detailed_look = input("Would you like a more detailed look into any of your stocks? ")
if detailed_look in ["y", "Y", "yes", "Yes"]:
    detailed_ticker = input("Which stock would you like to look at? (Remember to put the ticker in all caps). ")
    if detailed_ticker not in stocks:
        print("Invalid selection")
        sys.exit()
    elif latest_prices.get(detailed_ticker) is None:
        print(f"I'm sorry, but something went wrong and we could not find any data for {detailed_ticker}.")
        sys.exit()
    else:
        try:
            detailed_stock_price = latest_prices[detailed_ticker]
            detailed_ticker_total_price = globals().get(f"{detailed_ticker}_price", 0)
            number_of_shares = int(float(detailed_ticker_total_price) / float(detailed_stock_price))
            print(f"The stock is worth ${detailed_stock_price}")
            print(f"The total amount owned is ${round(float(detailed_ticker_total_price), 2)}")
            print(f"You own {number_of_shares} shares")
        except Exception:
            print(f"I'm sorry, but something went wrong and we could not find any data for {detailed_ticker}.")
