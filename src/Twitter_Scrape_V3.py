import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

writer = pd.ExcelWriter('Twitter_Result.xlsx', engine='xlsxwriter')  # name of the output file
xls = pd.ExcelFile('./results/Social_Media_URLs.xlsx')  # name of the source file
countries = ['MY', 'ID', 'PH', 'SG']  # sheets of the source file

username = []
bad_url = []
browser_options = Options()
browser_options.add_argument('--headless')
browser = webdriver.Remote('http://selenium-chrome:4444/wd/hub', options=browser_options)

for country in countries:
    df1 = pd.read_excel(xls, country)
    companies = []
    follower_list = []

    for i in range(0, len(df1)):
        print('running on ' + country)

        try:
            company = str(df1.iloc[i]['Twitter']).split("/")
            company = company[3]
            url = 'https://www.twitter.com/' + company
            browser.get(url)
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            f = soup.find_all('span',
                              attrs={'class': 'css-901oao css-16my406 r-1fmj7o5 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0'})
            follower = f[1].find('span', attrs={'class': 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
            num_followers = str(follower)[64:str(follower).find('</span>')]
            follower_list.append(num_followers)
            companies.append(df1.iloc[i]['Company'])
        except:
            bad_url.append(url)
            follower_list.append(0)
            companies.append(df1.iloc[i]['Company'])

    finaldf = pd.DataFrame(df1.Twitter)
    finaldf['Twitter_account'] = companies
    finaldf['Followers'] = follower_list
    finaldf = finaldf[['Twitter_account', 'Twitter', 'Followers']]
    finaldf.to_excel(writer, sheet_name=country, index=False)

writer.save()
# close browser to release memory
browser.quit()
