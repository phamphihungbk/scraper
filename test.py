from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup

my_url = 'https://www.facebook.com/altheamalaysia/'
browser_options = Options()
browser_options.add_argument('--headless')
browser = webdriver.Firefox(options=browser_options)
print(browser)
browser.get(my_url)
time.sleep(1)
soup = BeautifulSoup(browser.page_source, 'lxml')
f = soup.find('div', attrs={'class': '_4-u3 _5sqi _5sqk'})
likes = f.find('span', attrs={'class': '_52id _50f5 _50f7'})  # finding span tag inside clas
num_followers = str(likes)[32:str(likes).find(' <span class="_50f8 _50f4 _5kx5">suka</span></span>')]
print(num_followers)
browser.quit()
