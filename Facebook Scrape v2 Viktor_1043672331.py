import requests
import csv 
import pandas as pd
from bs4 import BeautifulSoup

xls = pd.ExcelFile('Social_Media_URLs.xlsx') #name of the source file
countries = ['MY','ID','PH','SG','VN','TH'] #sheets of the source file

username = []

bad_urls = []

writer = pd.ExcelWriter('FBtest1.xlsx', engine = 'xlsxwriter') #name of the OUTPUT


for country in countries:
    
    
    df1 = pd.read_excel(xls,country) # --- LOOPing the countries



    companies = []
    follower_list = []
    
    df1.columns = ['Facebook' if col == 'FCB' else col for col in df1.columns]
    for i in range(0, len(df1)): #length of the data frame
       
        
        try:
           company = str(df1.iloc[i]['Facebook']).split("/")
           company = company[3]
           url = 'https://www.facebook.com/'+ company
           r = requests.get(url)
           soup = BeautifulSoup(r.content,'lxml') #Beautiful Soup library
           f = soup.find('div', attrs={'class': '_4-u3 _5sqi _5sqk'})
           likes=f.find('span',attrs={'class':'_52id _50f5 _50f7'}) #finding span tag inside clas
           num_followers = str(likes)[32:str(likes).find(' <span class="_50f8 _50f4 _5kx5">suka</span></span>')]
           follower_list.append(num_followers)
           companies.append(df1.iloc[i]['Company'])
           #  ----> Adding Rows
        except:
           bad_urls.append(url)
           follower_list.append(0)
           companies.append(df1.iloc[i]['Company'])
           
           
           
           
    finaldf = pd.DataFrame(df1.Facebook)
    finaldf['facebook_acc']=companies
    finaldf['followers']=follower_list
    finaldf = finaldf[['facebook_acc','Facebook','followers']]
        

    finaldf.to_excel(writer, sheet_name = country,index = False)

writer.save() #final writing to Excel


