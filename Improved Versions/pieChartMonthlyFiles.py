import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def loadData(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    return df

def pieChart(df):
    print(len(df["Filing Date"]))
    df['Month'] = df['Filing Date'].dt.strftime('%B')
    monthly_counts = df['Month'].value_counts()
    plt.figure(figsize=(10, 7))
    plt.pie(monthly_counts, labels=monthly_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('2023: Number of Trades Filed in Each Month')
    plt.show()


def main():
    csv = "/Users/leofeingold/Desktop/open insider 2/CSV Folders/2023Scrape.csv"
    data = loadData(csv)
    pieChart(data)

if __name__ == "__main__":
    main()