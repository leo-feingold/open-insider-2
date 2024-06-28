import matplotlib.pyplot as plt
import pandas as pd

path = "/Users/leofeingold/Desktop/open insider 2/Dec2018ResultsUpwardMomentum.csv"
df = pd.read_csv(path)

'''
print(f"Columns: {df.columns}")
corr = df["Return on Investment"].corr(df["Market Cap"])
print(f"Correlation: {corr}")

plt.scatter(df["Return on Investment"], df["Market Cap"])
plt.title(f"2023 ROI vs Market Cap, Correlation: {corr}, Size: {len(df)} Stocks")
plt.xlabel("ROI")
plt.ylabel("Market Cap")
plt.show()
'''

df["Amount Made"] = df["Return on Investment"] * 100
sum = df["Amount Made"].sum()
print(f"Sum: {sum}")