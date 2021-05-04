import re

import pandas as pd
import requests

xls = pd.ExcelFile('Social_Media_URLs.xlsx')
countries = ['MY', 'ID', 'PH', 'SG', 'VN', 'TH']

username = []
bad_urls = []

writer = pd.ExcelWriter('Instagram_test4jul.xlsx', engine='xlsxwriter')

for country in countries:
    df1 = pd.read_excel(xls, country)  # --- LOOPing the countries

    companies = []
    follower_list = []

    df1.columns = ['Instagram' if col == 'IG' else col for col in df1.columns]
    for i in range(0, len(df1)):  # length of the data frame

        try:
            company = str(df1.iloc[i]['Instagram']).split("/")
            company = company[3]
            url = 'https://www.instagram.com/' + company
            r = requests.get(url)
            m = re.search(r'"edge_followed_by":\{"count":([0-9]+)\}', str(r.content))
            num_followers = m.group(1)
            follower_list.append(num_followers)
            companies.append(df1.iloc[i]['Company'])

        except:
            bad_urls.append(url)
            follower_list.append(1)
            companies.append(df1.iloc[i]['Company'])

    finaldf = pd.DataFrame(df1.Instagram)
    finaldf['instagram_account'] = companies
    finaldf['followers'] = follower_list
    finaldf = finaldf[['instagram_account', 'Instagram', 'followers']]

    finaldf.to_excel(writer, sheet_name=country, index=False)

writer.save()  # final writing to Excel
