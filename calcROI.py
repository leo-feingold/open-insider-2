import pandas as pd
import numpy as np

def load_data(csv):
    df = pd.read_csv(csv)
    df = df.sort_values("Actual Purchase Date", ascending=True)
    return df

def group_data(df):
    grouped_data = df.groupby(["Actual Purchase Date", "Timing"])
    return grouped_data

def calc_roi(df, initial_capital):
    investment_per_group = initial_capital/6
    grouped_df = group_data(df)
    grouped_df["Liquid Cash"] = initial_capital - investment_per_group



def main():
    path = "/Users/leofeingold/Desktop/open insider 2/Results, Market Cap Filtered For Momentum/2023ResultsMomentumGood.csv"
    data = load_data(path)
    print(data.head(-1))
    grouped_data = group_data(data)
    group_sizes = grouped_data.size()
    print(group_sizes["2023-01-03", "Open"])


if __name__ == "__main__":
    main()