from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta


#main_url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=02%2F13%2F2023+-+02%2F14%2F2023&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"

def scrape_data(start_date, end_date):
    max_page = 9
    driver = webdriver.Safari()
    driver.implicitly_wait(10)
    dfs = []
    page = 1

    while page < max_page + 1:
        url = f"http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={start_date}+-+{end_date}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page={page}"
        try:
            driver.get(url)
            print(f"Page {page}:")
            print(f"URL: {url}")
            table = driver.find_element(By.CLASS_NAME, 'tinytable')
            print(f"Found Table. Begining scrape of page {page}.")
            rows = table.find_elements(By.TAG_NAME, 'tr')
            data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if not cells:
                    cells = row.find_elements(By.TAG_NAME, 'th')
                data.append([cell.text for cell in cells])

            print(f"Finished scraping page {page}. Saving Data")
            df = pd.DataFrame(data[1:], columns=data[0])
            print(f"Data from page {page}: \n{df.head(-1)}")
            dfs.append(df)
            page += 1

        except Exception as e:
            print(f"Scraped all data or encountered an error. \nCorresponding Error Message: \n{e}")
            break
    
    print(f"Scraped first {page - 1} pages of data between {start_date} and {end_date}.")
    driver.quit()
    return dfs

def concat_and_finish(dfs):
    final_df = pd.concat(dfs, ignore_index=True)
    print(f"Columns: {final_df.columns}")
    print(f"Result: {final_df}")
    final_df.to_csv("Dec2021Scrape.csv", index=False)

def main():
    min_date = datetime(2021, 12, 2).date()
    max_date = datetime(2021, 12, 31).date()

    dfs = scrape_data(min_date, max_date)
    if dfs:
        concat_and_finish(dfs)
    else:
        print("No data was scraped.")

if __name__ == "__main__":
    main()
