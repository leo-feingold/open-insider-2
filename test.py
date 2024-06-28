import pandas as pd
import numpy as np

def load_data(csv):
    df = pd.read_csv(csv, keep_default_na=False, na_values=[""])
    df = df.sort_values("Actual Purchase Date", ascending=True)
    print(df.head(8))
  
    grouped_df = df.groupby(["Actual Purchase Date", "Timing"]).size().unstack(fill_value=0)
    grouped_df = grouped_df.rename(columns={"Open": "Open Count", "Close": "Close Count"}) 
 
    df = df.merge(grouped_df, on="Actual Purchase Date", how="left")
    df["Investment Size"] = df.apply(lambda row: row["Open Count"] if row["Timing"] == "Open" else row["Close Count"], axis=1)
    
    print(df.head(8))
    return df

def buys_and_sells_by_day(df, intial_capital):
    capital_per_day = intial_capital/6
    unique_dates = df["Actual Purchase Date"].unique()
    transactions = []

    for date in unique_dates:
        buy_condition = (df["Actual Purchase Date"] == date)
        sell_condition = (df["Sell Date"] == date)
        
        if buy_condition.any():
            buy_tickers = df.loc[buy_condition, ["Ticker", "Timing"]]
            num_buys = len(buy_tickers)
            investment = capital_per_day/num_buys
            for _, row in buy_tickers.iterrows():
                transactions.append({"Date": date,
                                    "Ticker": row['Ticker'],
                                    "Action": "Bought",
                                    "Timing": row['Timing'],
                                    "Change in Liquidity": -1*investment})
        
        if sell_condition.any():
            sell_tickers = df.loc[sell_condition, ["Ticker", "Return on Investment"]]
            for _, row in sell_tickers.iterrows():
                transactions.append({"Date": date,
                                    "Ticker": row['Ticker'],
                                    "Action": "Sold",
                                    "Timing": "Open",
                                    "Change in Liquidity": investment+100*row["Return on Investment"]})
    
    transactions_df = pd.DataFrame(transactions)
    return transactions_df


def main():
    path = "/Users/leofeingold/Desktop/open insider 2/Results, Market Cap Filtered For Momentum/2023ResultsMomentumGood.csv"
    data = load_data(path)
    #buys_and_sells = buys_and_sells_by_day(data, 10000)
    #specific_date_transactions = buys_and_sells[buys_and_sells["Date"] == "2023-01-09"]

if __name__ == "__main__":
    main()