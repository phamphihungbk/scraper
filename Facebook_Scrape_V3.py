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
            likes = soup.find('div', attrs={'class': '_4-u2 _6590 _3xaf _4-u8'})
            likes = likes.find_all('div', attrs={'class': '_2pi9 _2pi2'})
            likes = likes[1].find('div', attrs={'class': '_4bl9'})
            num_followers = str(likes)[24:str(likes).find(' orang mengikuti ini</div></div>')]
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
