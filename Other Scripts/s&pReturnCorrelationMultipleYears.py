import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

def loadData(sp500, insiders, sp, ins):
    sp500_df = pd.read_csv(sp500)
    insiders_df = pd.read_csv(insiders)
    sp_df = pd.read_csv(sp)
    ins_df = pd.read_csv(ins)
    return sp500_df, insiders_df, sp_df, ins_df

def alignData(sp500_df, insiders_df, sp_df, ins_df): 
    sp500_df['Month'] = sp500_df['Month'].str.strip()
    insiders_df['Month'] = insiders_df['Month'].str.strip()
    sp_df['Month'] = sp_df['Month'].str.strip()
    ins_df['Month'] = ins_df['Month'].str.strip()
   
    merged_df1 = pd.merge(sp500_df, insiders_df, on='Month', suffixes=('_sp500_2018', '_insider_2018'))
    merged_df2 = pd.merge(sp_df, ins_df, on='Month', suffixes=('_sp500_2022', '_insider_2022'))
    merged_df = pd.concat([merged_df1, merged_df2])

    return merged_df


def calcCorr(df):
    corr_2018 = df["ROI_sp500_2018"].corr(df["ROI_insider_2018"])
    corr_2022 = df["ROI_sp500_2022"].corr(df["ROI_insider_2022"])

    combined_sp500_roi = pd.concat([df["ROI_sp500_2018"], df["ROI_sp500_2022"]])
    combined_insider_roi = pd.concat([df["ROI_insider_2018"], df["ROI_insider_2022"]])
    combined_corr = combined_sp500_roi.corr(combined_insider_roi)

    print(f"Combined Correlation: {combined_corr}")
    print(f"Combined r^2: {combined_corr**2}")
    print(f"Correlation 2018: {corr_2018}")
    print(f"r^2 2018: {corr_2018**2}")
    print(f"Correlation 2022: {corr_2022}")
    print(f"r^2 2022: {corr_2022**2}")

    return combined_corr, corr_2018, corr_2022, 


def plotData(df, combo):    
    unique_months = df["Month"].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_months)))
    color_map = dict(zip(unique_months, colors))

    plt.figure(figsize=(8, 6))
    
    for month in unique_months:
        month_data_2018 = df[df['Month'] == month]
        month_data_2022 = df[df['Month'] == month]
        plt.scatter(month_data_2018["ROI_sp500_2018"], month_data_2018["ROI_insider_2018"], label=f'{month} 2018', color=color_map[month])
        plt.scatter(month_data_2022["ROI_sp500_2022"], month_data_2022["ROI_insider_2022"], label=f'{month} 2022', color=color_map[month], marker='x')


    plt.xlabel('S&P 500 ROI (%)')
    plt.ylabel('Strategy ROI (%)')
    plt.title(f"r^2 = {combo**2}")
    plt.suptitle(f'Correlation between S&P 500 and Strategy ROI (x: 2022, o: 2018)')
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[month], markersize=10, label=month) for month in unique_months]
    plt.legend(handles=handles, title="Month", bbox_to_anchor=(1, 1), loc='upper left', fontsize='medium')
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.95, 1])
    plt.show()

def main():
    sp500 = "/Users/leofeingold/Desktop/open insider 2/sp500_monthly_performance_2018.csv"
    insiders = "/Users/leofeingold/Desktop/open insider 2/2018_returns_by_month.csv"
    sp1 = "/Users/leofeingold/Desktop/open insider 2/sp500_monthly_performance_2022.csv"
    ins1 = "/Users/leofeingold/Desktop/open insider 2/2022_returns_by_month.csv"
    sp500_df, insiders_df, sp, ins = loadData(sp500, insiders, sp1, ins1)
    merged_df = alignData(sp500_df, insiders_df, sp, ins)
    combined, a, b = calcCorr(merged_df)
    plotData(merged_df, combined)

if __name__ == "__main__":
    main()