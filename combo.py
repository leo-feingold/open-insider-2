import pandas as pd

csv1 = "/Users/leofeingold/Desktop/open insider 2/JanToApril2018Scrape.csv"
csv2 = "/Users/leofeingold/Desktop/open insider 2/AprilToMidAugust2018Scrape.csv"
csv3 = "/Users/leofeingold/Desktop/open insider 2/MidAugustToDec2018Scrape.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)

merged_df  = pd.concat([df3, df2, df1], ignore_index=True)
merged_df.to_csv("2018Scrape.csv", index=False)