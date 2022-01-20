import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# name of the output file
writer = pd.ExcelWriter('../results/Instagram_Result.xlsx', engine='xlsxwriter')
# name of the source file
xls = pd.ExcelFile('Social_Media_URLs.xlsx')
# sheets of the source file
countries = ['MY', 'ID', 'PH', 'SG', 'VN', 'TH']

username = []
bad_urls = []
bs_options = Options()
bs_options.add_argument('--headless')
bs_options.add_argument('--lang=en')
browser = webdriver.Remote(
	'http://selenium-chrome:4444/wd/hub',
	options=bs_options
)

browser.get('https://www.instagram.com/accounts/login/')
time.sleep(4)
usr = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input')
password = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input')
submit = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button')

# need to put your instagram account to login
usr.send_keys('')
password.send_keys('')
submit.click()

# wait for login in
time.sleep(5)

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
            time.sleep(1)
            browser.get(url)
            time.sleep(1)
            m = re.search(r'"edge_followed_by":\{"count":([0-9]+)\}', str(browser.page_source))
            num_followers = m.group(1)
            print(num_followers)
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
