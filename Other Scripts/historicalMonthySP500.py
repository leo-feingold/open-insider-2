import yfinance as yf
import pandas as pd

sp500 = yf.download('^GSPC', start='2021-1-01', end='2021-12-31')
monthly_data = sp500['Adj Close'].resample('ME').ffill()
monthly_returns = monthly_data.pct_change().dropna() * 100

monthly_performance = pd.DataFrame({
    'Month': monthly_returns.index.strftime('%B'),
    'ROI': monthly_returns.values
})

output_file_path = 'sp500_monthly_performance_2021.csv'
monthly_performance.to_csv(output_file_path, index=False)

print(f"Monthly performance data saved to {output_file_path}")
