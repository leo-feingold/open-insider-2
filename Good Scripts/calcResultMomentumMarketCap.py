import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import timedelta, time, datetime, date
import matplotlib.pyplot as plt
import ta

def loadData(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'], errors='coerce')
    df['Ticker'] = df['Ticker'].str.strip()
    return df

def isTradingDay(data, target_date):
    target_date = pd.to_datetime(target_date).normalize()
    return not data.index[data.index == target_date].empty

def findNearestFutureDay(data, target_date):
    target_date = pd.to_datetime(target_date).normalize()
    future_dates = data.index[data.index >= target_date]
    if not future_dates.empty:
        closest_date = future_dates[0]
    else:
        closest_date = data.index[-1]
    return closest_date

def identify_downward_momentum(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    
    df['Downward_Momentum'] = (df['RSI'] < 30) & (df['MACD'] < df['MACD_Signal'])
    return df

def calcSellDate(data, actual_purchase_date, timing):
    market_days_passed = 1 if timing == "Open" else 0
    curr_sell_date = actual_purchase_date
    max_date_limit = pd.Timestamp.max - timedelta(days=3)  # three days before max to avoid overflow
    while market_days_passed <= 3:
        curr_sell_date += timedelta(days=1)
        if curr_sell_date >= max_date_limit:
            raise OverflowError("Sell date for exceeds maximum allowable datetime range.")
        if isTradingDay(data, curr_sell_date):
            market_days_passed += 1
    return findNearestFutureDay(data, curr_sell_date)

def get_market_cap(stock, data, date):
    date = pd.to_datetime(date).normalize()
    if not isTradingDay(data, date):
        print(f"Date {date} is not a trading day for ticker {stock}.")
        return 0

    if date not in data.index.normalize():
        print(f"No data available for {stock} on {date}.")
        return 0

    closing_price = data.loc[date, 'Close']

    try:
        shares_outstanding = stock.info.get('sharesOutstanding')
    except Exception as e:
        print(f"Error fetching shares outstanding for {stock}: {e}")
        return 0

    if shares_outstanding is None:
        print(f"Shares outstanding information not available for {stock}.")
        return 0
    
    market_cap = closing_price * shares_outstanding
    return market_cap

def determinePerformance(df):
    num_no_data = 0
    num_error_loading = 0
    num_down_momentum = 0
    market_open = time(9, 30)
    market_close = time(16, 0)
    result_df = pd.DataFrame(columns=["Ticker", "Market Cap", "Filing Date", "Actual Purchase Date", "Timing", "Purchase Price", "Sell Date", "Sell Price", "Return on Investment"])
    down_momentum_df = pd.DataFrame(columns=["Ticker", "Filing Date"])

    for stock, filing_date in zip(df["Ticker"], df["Filing Date"]):
        if pd.isna(stock) or not isinstance(stock, str):
            print(f"Invalid ticker: {stock}, skipping entry")
            continue
        stock = stock.strip().upper()  # Ensure ticker is clean and uppercase
        start_date_yf = filing_date - timedelta(days=70)
        end_date_yf = filing_date + timedelta(days=20)

        try:
            data = yf.download(stock, start=start_date_yf, end=end_date_yf)
            if data.empty:
                print(f"No data found for ticker: {stock}, skipping entry")
                num_no_data += 1
                continue
        except Exception as e:
            print(f"Error downloading data for {stock}: {e}, skipping entry")
            num_error_loading += 1
            continue

        if not data.empty:
            data = identify_downward_momentum(data)
            downward_momentum_period = data.loc[filing_date - timedelta(days=10):filing_date - timedelta(days=1)]
            
            if downward_momentum_period['Downward_Momentum'].any():
                print(f"Downward momentum detected within 10 days before {filing_date} for {stock}, skipping purchase")
                num_down_momentum += 1
                down_momentum_df = pd.concat([down_momentum_df, pd.DataFrame({
                    "Ticker": [stock],
                    "Filing Date": [filing_date]
                })], ignore_index=True)
                continue

            if filing_date.time() > market_close:
                target_purchase_date = filing_date + timedelta(days=1)
                timing = "Open"
            elif filing_date.time() < market_open:
                target_purchase_date = filing_date
                timing = "Open"
            else:
                target_purchase_date = filing_date
                timing = "Close"

            actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
            open_price = data.loc[actual_purchase_date]["Open"] if timing == "Open" else data.loc[actual_purchase_date]["Close"]

            try:
                sell_date = calcSellDate(data, actual_purchase_date, timing)
            except OverflowError as e:
                print(f"Error calculating sell date for {stock}: {e}, skipping entry")
                continue

            close_price = data.loc[sell_date]["Open"]
            roi = ((close_price - open_price) / open_price)

            try:
                stock_info = yf.Ticker(stock)
                market_cap = get_market_cap(stock_info, data, actual_purchase_date)
                print(f"Found Market Cap For {stock}: {market_cap}")
            except ValueError as e:
                print(e)
                continue

            if True:
                print(f"Adding Stock: {stock}, {timing} of {pd.to_datetime(actual_purchase_date).date()}")
                result_df = pd.concat([result_df, pd.DataFrame({
                    "Ticker": [stock],
                    "Market Cap": [market_cap],
                    "Filing Date": [filing_date],
                    "Actual Purchase Date": [actual_purchase_date],
                    "Timing": timing,
                    "Purchase Price": [open_price],
                    "Sell Date": [sell_date],
                    "Sell Price": [close_price],
                    "Return on Investment": [roi]
                })], ignore_index=True)

    print(f"Num Error Loading: {num_error_loading}")
    print(f"Num No Data: {num_no_data}")
    print(f"Num Downwards Momentum: {num_down_momentum}")
    return result_df, down_momentum_df

def visualizeData(results_df):
    if results_df.empty:
        print("No data to visualize.")
        return

    results_df = results_df.sort_values("Actual Purchase Date")
    daily_roi = results_df.groupby("Actual Purchase Date")["Return on Investment"].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(daily_roi["Actual Purchase Date"], daily_roi["Return on Investment"], color='black')
    
    total_roi_sum = daily_roi["Return on Investment"].sum()
    plt.title(f"Daily ROI Over Time (Total Summed ROI (NOT NET ROI): {total_roi_sum:.3f}%)")
    plt.xlabel("Purchase Date")
    plt.ylabel("Summed ROI")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    csv = "/Users/leofeingold/Desktop/open insider 2/Scraped Data/2021Scrape.csv"
    insiders = loadData(csv)
    results, bad_momentum_df = determinePerformance(insiders)
    print(results)
    results.to_csv("2021ResultsMomentumGood.csv", index=False)
    bad_momentum_df.to_csv("2021BadMomentumStocks.csv", index=False)
    visualizeData(results)

if __name__ == "__main__":
    main()
