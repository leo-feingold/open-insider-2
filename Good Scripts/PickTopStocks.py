import pandas as pd
import warnings
warnings.filterwarnings("ignore")

scrapePath = "/Users/leofeingold/Desktop/open insider 2/2022Scrape.csv"
resultsPath = "/Users/leofeingold/Desktop/open insider 2/2022ResultsMomentumGood.csv"

scrape_df = pd.read_csv(scrapePath)
scrape_df.columns = scrape_df.columns.str.replace('\xa0', ' ').str.strip()
scrape_df['Ticker'] = scrape_df['Ticker'].str.strip().str.upper()

#scrape_df['Filing Date'] = pd.to_datetime(scrape_df['Filing Date'])
#scrape_df = scrape_df[['Ticker', 'Filing Date', 'Title']]

results_df = pd.read_csv(resultsPath)

merged_df = pd.merge(scrape_df, results_df, on=['Ticker', 'Filing Date'])
merged_df["Amount Made"] = merged_df["Return on Investment"] * 100

total_made_init = merged_df['Amount Made'].sum()
len_init = len(merged_df)
print(f"Intial: {merged_df.head(-1)}")
print(f"Intial Amount Made: {total_made_init}")
print(f"Length: {len_init}")

old_ratio = total_made_init/len_init
print(f"Ratio: {old_ratio}")

#merged_df.to_csv("merged_exp.csv")



important_positions_contains = [
    "Chairman",
    "CHRMN"
    "CEO",
    "CFO",
    "COB",
    "Pres",
    "COO",
    "EVP",
    "SVP",
    "Chief Financial Officer",
    "Chief Executive Officer",
    "Chief Operating Officer",
    "Chief Strategy Officer",
    "Chief Marketing Officer",
    "Chief Revenue Officer",
    "Chief Commercial Officer",
    "Chief Development Officer",
    "Chief Growth Officer",
    "Chief People Officer",
    "Chief Administrative Officer",
    "Chief Legal Officer",
    "Chief Technology Officer",
    "Chief Information Officer",
    "Chief Scientific Officer",
    "VP",
    "Chief Supply Chain Officer",
    "Chief Operations Officer",
    "CHIEF INVESTMENT OFFICER",
    "Chief Product Officer",
    "Chief Acquisition Officer"
    "Chief Tech"

]

important_pattern_contains = '|'.join(important_positions_contains)
#ignore_pattern = '|'.join(important_positions_ignore)

data_filtered = merged_df[merged_df["Title"].str.contains(important_pattern_contains, case=False, na=False)]
#data_filtered = data_filtered[~data_filtered["Title"].str.contains(ignore_pattern, case=False, na=False)]

data_filtered['Value'] = data_filtered['Value'].str.replace('$', '')
data_filtered['Value'] = data_filtered['Value'].str.replace(',', '')
data_filtered['Value'] = data_filtered['Value'].str.replace('+', '')
data_filtered["Value"] = pd.to_numeric(data_filtered["Value"])
data_filtered = data_filtered[data_filtered["Value"] > 10000]

data_filtered.reset_index(drop=True, inplace=True)


total_made_new = data_filtered['Amount Made'].sum()
len_new = len(data_filtered)
print(f"\nNew: {data_filtered.head(-1)}")
print(f"New Amount Made: {total_made_new}")
print(f"Length: {len_new}")

new_ratio = total_made_new/len_new
print(f"Ratio: {new_ratio}")

if new_ratio > old_ratio: print("Good Filter")
else: print("Bad Filter")


#initial_titles = set(merged_df["Title"].unique())
#filtered_titles = set(data_filtered["Title"].unique())
#excluded_titles = initial_titles - filtered_titles
#print(f"Excluded Titles: {excluded_titles}")