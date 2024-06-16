import pandas as pd

csv1 = "/Users/leofeingold/Desktop/open insider 2/JanToApril2021Scrape.csv"
csv2 = "/Users/leofeingold/Desktop/open insider 2/AprilToAugust2021Scrape.csv"
csv3 = "/Users/leofeingold/Desktop/open insider 2/AugustToDec2021Scrape.csv"
csv4 = "/Users/leofeingold/Desktop/open insider 2/Dec2021Scrape.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df3 = pd.read_csv(csv3)
df4 = pd.read_csv(csv4)

merged_df  = pd.concat([df4, df3, df2, df1], ignore_index=True)
merged_df.to_csv("2021Scrape.csv", index=False)