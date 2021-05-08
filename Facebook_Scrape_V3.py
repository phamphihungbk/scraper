import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

writer = pd.ExcelWriter('Facebook_Result.xlsx', engine='xlsxwriter')  # name of the output file
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
    df1.columns = ['Facebook' if col == 'FCB' else col for col in df1.columns]

    for i in range(0, len(df1)):
        print('running on ' + country)

        try:
            company = str(df1.iloc[i]['Facebook']).split("/")
            company = company[3]
            url = 'https://www.facebook.com/' + company
            browser.get(url)
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            likes = soup.find('span', attrs={'class': '_52id _50f5 _50f7'})
            num_followers = str(likes)[32:str(likes).find(' <span class="_50f8 _50f4 _5kx5">suka</span></span>')]
            follower_list.append(num_followers)
            companies.append(df1.iloc[i]['Company'])

        except:
            bad_urls.append(url)
            follower_list.append(0)
            companies.append(df1.iloc[i]['Company'])

    finaldf = pd.DataFrame(df1.Facebook)
    finaldf['Facebook_acc'] = companies
    finaldf['Followers'] = follower_list
    finaldf = finaldf[['Facebook_acc', 'Facebook', 'Followers']]
    finaldf.to_excel(writer, sheet_name=country, index=False)

writer.save()
# close browser to release memory
browser.quit()
