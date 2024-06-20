import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def loadData(sp500, insiders):
    sp500_df = pd.read_csv(sp500)
    insiders_df = pd.read_csv(insiders)
    return sp500_df, insiders_df

def alignData(sp500_df, insiders_df): 
    sp500_df['Month'] = sp500_df['Month'].str.strip()
    insiders_df['Month'] = insiders_df['Month'].str.strip()
   
    merged_df = pd.merge(sp500_df, insiders_df, on='Month', suffixes=('_sp500', '_insider'))

    return merged_df


def calcCorr(df):
    corr = df["ROI_sp500"].corr(df["ROI_insider"])
    
    print(f"Correlation: {corr}")
    print(f"r^2: {corr**2}")

    return corr 


def plotData(df, combo):    
    unique_months = df["Month"].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_months)))
    color_map = dict(zip(unique_months, colors))

    plt.figure(figsize=(8, 6))
    
    for month in unique_months:
        month_data = df[df['Month'] == month]
        plt.scatter(month_data["ROI_sp500"], month_data["ROI_insider"], label=f'{month}', color=color_map[month])


    plt.xlabel('S&P 500 ROI (%)')
    plt.ylabel('Strategy ROI (%)')
    plt.title(f"r^2 = {combo**2}")
    plt.suptitle(f'2021 Correlation between S&P 500 and Strategy ROI')
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[month], markersize=10, label=month) for month in unique_months]
    plt.legend(handles=handles, title="Month", bbox_to_anchor=(1, 1), loc='upper left', fontsize='medium')
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.95, 1])
    plt.show()

def main():
    sp500 = "/Users/leofeingold/Desktop/open insider 2/sp500_monthly_performance_2021.csv"
    insiders = "/Users/leofeingold/Desktop/open insider 2/2021_returns_by_month.csv"
    sp500_df, insiders_df = loadData(sp500, insiders)
    merged_df = alignData(sp500_df, insiders_df)
    combined = calcCorr(merged_df)
    plotData(merged_df, combined)

if __name__ == "__main__":
    main()