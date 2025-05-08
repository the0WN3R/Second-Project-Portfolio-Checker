import yfinance as yf
import requests.exceptions
import sys

stocks = ["ADBE", "BA", "DELL", "DIA", "DLTR", "LLY", "MSFT", "QQQ", "SPY", "TMUS", "YETI"]

for stock in stocks:
    try:
        print(f"{stock}: ${(yf.Ticker(stock)).info.get("regularMarketPrice")}")
    except requests.exceptions.HTTPError:
        print("Could not locate stock price")

ADBE_price = (yf.Ticker(stocks[0])).info.get("regularMarketPrice")
BA_price = (yf.Ticker(stocks[1])).info.get("regularMarketPrice")
DELL_price = (((yf.Ticker(stocks[2])).info.get("regularMarketPrice")) * 5)
DIA_price = (yf.Ticker(stocks[3])).info.get("regularMarketPrice")
DLTR_price = (yf.Ticker(stocks[4])).info.get("regularMarketPrice")
LLY_price = (yf.Ticker(stocks[5])).info.get("regularMarketPrice")
MSFT_price = (yf.Ticker(stocks[6])).info.get("regularMarketPrice")
QQQ_price = (yf.Ticker(stocks[7])).info.get("regularMarketPrice")
SPY_price = (((yf.Ticker(stocks[8])).info.get("regularMarketPrice"))*7)
TMUS_price = (((yf.Ticker(stocks[9])).info.get("regularMarketPrice"))*2)
YETI_price = (((yf.Ticker(stocks[10])).info.get("regularMarketPrice"))*8)

portfolio_value = ADBE_price + BA_price + DELL_price + DIA_price + DLTR_price + LLY_price + MSFT_price + QQQ_price + SPY_price + TMUS_price + YETI_price
with open("portfolio.txt") as file:
    previous_portfolio_value = float(file.read().strip())

print(f"Your net gain/loss today was: ${round(portfolio_value - previous_portfolio_value, 2)}")

with open("portfolio.txt", "w") as file2:
    file2.write(str(portfolio_value))

if input("Would you like a more detailed look into any of your stocks? ") in ["y", "Y", "yes", "Yes"]:
    detailed_ticker = input("Which stock would you like to look at? (Remember to put the ticker in all caps). ")
    if detailed_ticker not in stocks:
        print("Invalid selection")
        sys.exit()
    else:
        detailed_stock = (yf.Ticker(detailed_ticker)).info.get("regularMarketPrice")
        detailed_ticker_owned = globals().get(f"{detailed_ticker}_price")
        number_of_shares = int(float(detailed_ticker_owned) / float(detailed_stock))
        print(f"The stock is worth {detailed_stock}")
        print(f"The total amount owned is {round(float(detailed_ticker_owned), 2)}")
        print(f"You own {number_of_shares} shares")
