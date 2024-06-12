import pandas as pd

csv1 = "/Users/leofeingold/Desktop/open insider 2/CSV Folders/2023JanThroughMayResults.csv"
csv2 = "/Users/leofeingold/Desktop/open insider 2/CSV Folders/2023JuneThroughDecResults.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

merged_df  = pd.concat([df2, df1], ignore_index=True)
merged_df.to_csv("2023Results.csv", index=False)