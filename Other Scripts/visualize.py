import numpy as np
import pandas as pd
import yfinance as yf
from datetime import timedelta, time, datetime
import matplotlib.pyplot as plt

def loadClusterBuys(csv):
    df = pd.read_csv(csv)
    print("Columns in the DataFrame:", df.columns.tolist())
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    print("Updated Columns in the DataFrame:", df.columns.tolist())
    return df

def findNearestFutureDay(data, target_date):
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    future_dates = data.index[data.index >= target_date]
    if not future_dates.empty:
        closest_date = future_dates[0]
    else:
        closest_date = data.index[-1]
    return closest_date

def performanceOverNext3Days(df):
    num_no_data = 0
    num_error_loading = 0
    market_open = time(9, 30)
    market_close = time(16, 0)
    result_df = pd.DataFrame(columns=["Ticker", "Filing Date", "Actual Purchase Date", "Purchase Price", "Sell Date", "Sell Price", "Return on Investment"])

    for stock, filing_date in zip(df["Ticker"], df["Filing Date"]):
        if pd.isna(stock) or not isinstance(stock, str):
            print(f"Invalid ticker: {stock}, skipping entry")
            continue
        start_date = filing_date - timedelta(days=1)
        end_date = filing_date + timedelta(days=9)


        try:
            data = yf.download(stock, start=start_date, end=end_date)
            if data.empty:
                print(f"No data found for ticker: {stock}, skipping entry")
                num_no_data += 1
                continue
        except Exception as e:
            print(f"Error downloading data for {stock}: {e}, skipping entry")
            num_error_loading += 1
            continue

        if not data.empty:
            if filing_date.time() > market_close:
                # filed after hours -> buy next days open
                target_purchase_date = filing_date + timedelta(days=1)
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Open"]
            elif filing_date.time() < market_open:
                # filed before opening -> buy that day's open
                target_purchase_date = filing_date
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Open"]
            else:
                # filed during the trading day -> buy at the close of that day (best I can do with YF)
                target_purchase_date = filing_date
                actual_purchase_date = findNearestFutureDay(data, target_purchase_date)
                open_price = data.loc[actual_purchase_date]["Close"]

            # still selling at close of day 3
            sell_date = findNearestFutureDay(data, actual_purchase_date + timedelta(days=3))
            close_price = data.loc[sell_date]["Close"]
            roi = ((close_price - open_price) / open_price)

            # no penny stocks
            if open_price > 1 and close_price > 1:
                result_df = pd.concat([result_df, pd.DataFrame({
                "Ticker": [stock],
                "Filing Date": [filing_date],
                "Actual Purchase Date": [actual_purchase_date],
                "Purchase Price": [open_price],
                "Sell Date": [sell_date],
                "Sell Price": [close_price],
                "Return on Investment": [roi]
            })], ignore_index=True)

    
    print(f"Num Error Loading: {num_error_loading}")
    print(f"Num No Data: {num_no_data}")
    return result_df

def visualizeData(results_df):
    results_df = results_df.sort_values("Actual Purchase Date")
    daily_roi = results_df.groupby("Actual Purchase Date")["Return on Investment"].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(daily_roi["Actual Purchase Date"], daily_roi["Return on Investment"], color='black')
    
    total_roi_sum = daily_roi["Return on Investment"].sum()
    plt.title(f"Daily ROI Over Time (Total ROI: {total_roi_sum:.3f}%)")
    plt.xlabel("Purchase Date")
    plt.ylabel("Summed ROI")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    '''
    csv = "/Users/leofeingold/Desktop/open insider 2/2016Scrape.csv"
    clusters = loadClusterBuys(csv)
    results = performanceOverNext3Days(clusters)
    print(results)
    results.to_csv("2016Results.csv", index=False)
    '''
    results = pd.read_csv("/Users/leofeingold/Desktop/open insider 2/CSV Folders pt. 2/2020Results.csv")
    visualizeData(results)


if __name__ == "__main__":
    main()
