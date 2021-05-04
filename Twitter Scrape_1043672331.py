import pandas as pd
import requests
from bs4 import BeautifulSoup

xls = pd.ExcelFile('Social_Media_URLs.xlsx')
countries = ['MY', 'ID', 'PH', 'SG']

username = []

bad_url = []

writer = pd.ExcelWriter('Twitter_test1Dec.xlsx', engine='xlsxwriter')  # Name of the output

for country in countries:
    df1 = pd.read_excel(xls, country)  # --- LOOPing the countries
    companies = []
    follower_list = []

    for i in range(0, len(df1)):  # length of the data frame
        try:
            company = str(df1.iloc[i]['Twitter']).split("/")
            company = company[3]
            url = 'https://www.twitter.com/' + company
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            f = soup.find('li', class_="ProfileNav-item--followers")
            title = f.find('a')['title']
            num_followers = int(title.split(' ')[0].replace(',', ''))
            #               t.writerow([user,num_followers])    #  ----> Adding Rows
            follower_list.append(num_followers)
            companies.append(df1.iloc[i]['Company'])
        except:
            bad_url.append(url)
            #               t.writerow([user,0])
            follower_list.append(0)
            companies.append(df1.iloc[i]['Company'])

    finaldf = pd.DataFrame(df1.Twitter)
    finaldf['twitter_account'] = companies
    finaldf['followers'] = follower_list
    finaldf = finaldf[['twitter_account', 'Twitter', 'followers']]

    finaldf.to_excel(writer, sheet_name=country, index=False)

writer.save()  # final writing to Excel
