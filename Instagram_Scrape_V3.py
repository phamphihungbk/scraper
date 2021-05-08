import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

writer = pd.ExcelWriter('Instagram_Result.xlsx', engine='xlsxwriter')  # name of the output file
xls = pd.ExcelFile('Social_Media_URLs.xlsx')  # name of the source file
countries = ['MY', 'ID', 'PH', 'SG', 'VN', 'TH']  # sheets of the source file

username = []
bad_urls = []
browser_options = Options()
browser_options.add_argument('--headless')
browser = webdriver.Firefox(options=browser_options)

for country in countries:
    df1 = pd.read_excel(xls, country)
    companies = []
    follower_list = []
    df1.columns = ['Instagram' if col == 'IG' else col for col in df1.columns]

    for i in range(0, len(df1)):
        print('running on ' + country)

        try:
            company = str(df1.iloc[i]['Instagram']).split("/")
            company = company[3]
            url = 'https://www.instagram.com/' + company
            browser.get(url)
            time.sleep(1)
            m = re.search(r'"edge_followed_by":\{"count":([0-9]+)\}', str(browser.page_source))
            num_followers = m.group(1)
            follower_list.append(num_followers)
            companies.append(df1.iloc[i]['Company'])

        except:
            bad_urls.append(url)
            follower_list.append(1)
            companies.append(df1.iloc[i]['Company'])

    finaldf = pd.DataFrame(df1.Instagram)
    finaldf['Instagram_account'] = companies
    finaldf['Followers'] = follower_list
    finaldf = finaldf[['Instagram_account', 'Instagram', 'Followers']]
    finaldf.to_excel(writer, sheet_name=country, index=False)

writer.save()
# close browser to release memory
browser.quit()
