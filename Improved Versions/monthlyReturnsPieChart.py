import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def loadData(csv):
    df = pd.read_csv(csv)
    df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    df["Actual Purchase Date"] = pd.to_datetime(df['Actual Purchase Date'])
    df["Return on Investment"] = pd.to_numeric(df["Return on Investment"], errors='coerce')
    df["Purchasing Month"] = df['Actual Purchase Date'].dt.strftime('%B')

    return df

def pieChart(df):
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    df['Purchasing Month'] = pd.Categorical(df['Purchasing Month'], categories=month_order, ordered=True)
    
    returns_by_month = df.groupby("Purchasing Month")["Return on Investment"].sum()
    returns_by_month = returns_by_month.sort_index()
    returns_by_month.to_csv('2023_returns_by_month.csv')

    positive_returns_by_month = returns_by_month[returns_by_month >= 0]
    negative_returns_by_month = returns_by_month[returns_by_month < 0].index.tolist()

    plt.figure(figsize=(10, 7))
    plt.pie(positive_returns_by_month, labels=positive_returns_by_month.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('2023: Percentage Of Positive Returns By Our Purchasing Month (Not ROI, But Percentage of Sum Of Positive ROI\'s)')

    textstr = 'Actual ROI\'s:\n' + '\n'.join([f"{month}: {returns_by_month[month]:.2f}" for month in negative_returns_by_month])
    plt.gcf().text(0.02, 0.02, textstr, fontsize=12, bbox=dict(facecolor='red', alpha=0.5))

    textstr2 = 'Actual ROI\'s:\n' + '\n'.join([f"{month}: {returns_by_month[month]:.2f}" for month in positive_returns_by_month.index])
    plt.gcf().text(0.98, 0.02, textstr2, fontsize=12, bbox=dict(facecolor='green', alpha=0.5), horizontalalignment='right')


    plt.show()

def main():
    csv = "/Users/leofeingold/Desktop/open insider 2/CSV Folders/2023Results.csv"
    df = loadData(csv)
    pieChart(df)

if __name__ == "__main__":
    main()