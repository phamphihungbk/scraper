import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

writer = pd.ExcelWriter('Twitter_Result.xlsx', engine='xlsxwriter')  # name of the output file
xls = pd.ExcelFile('Social_Media_URLs.xlsx')  # name of the source file
countries = ['MY', 'ID', 'PH', 'SG']  # sheets of the source file

username = []
bad_url = []
browser_options = Options()
browser_options.add_argument('--headless')
browser = webdriver.Firefox(options=browser_options)

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
            f = soup.find('li', class_="ProfileNav-item--followers")
            title = f.find('a')['title']
            num_followers = int(title.split(' ')[0].replace(',', ''))
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
