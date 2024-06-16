import pandas as pd

csv = "/Users/leofeingold/Desktop/open insider 2/CSV Folders pt. 2/2021Results.csv"
df = pd.read_csv(csv)

df["Actual Purchase Date"] = pd.to_datetime(df["Actual Purchase Date"]).dt.date
grouped_df = df.groupby("Actual Purchase Date")["Return on Investment"].sum().reset_index()
grouped_df.columns = ['Date', 'ROI']
grouped_df.to_csv("2021DailyROI.csv")
print(grouped_df.head(-1))