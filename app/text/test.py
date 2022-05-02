from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from csv import DictWriter
import csv


options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Selenium サーバーへ接続する。
driver = webdriver.Remote(

    command_executor=os.environ["SELENIUM_URL"],
    desired_capabilities=options.to_capabilities(),
    options=options,

)

# 変数
print('検索キーワード入れろ')
q = input('>>')
url = f'https://www.youtube.com/results?search_query={q}&sp=EgIQAg%253D%253D'
#url = 'https://muuuuu.org'
base_url = 'https://www.youtube.com'
hikaku = []
with open('ccv_dict2.csv', 'r') as ff:
        reader = csv.DictReader(ff)
        z = [row for row in reader]

for x in z:
    c = x['name']
    hikaku.append(c)


driver.get(url)
time.sleep(15)
#ブラウザのウインドウ高を取得する
#81332
for x in range(1, 81332):
    
    driver.execute_script("window.scrollTo(0, "+str(x)+");")
    driver.execute_script("return window.innerHeight")
    print(x)


time.sleep(5)
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')
labels = ['url', 'name', 'vido']
dct_arr = []

for z in soup.select("#main-link"):
    r = z.get('href')
    key= z.select_one('#text').text
    c = z.select_one('#video-count').text
    urls = {'url':f'{base_url}{r}', 'name':key, 'vido':c }
    dct_arr.append(urls)

with open('ccv_dict2.csv', 'a', newline='') as f:
    writer = DictWriter(f, fieldnames=labels)
    for elem in dct_arr:
        if elem['name'] not in hikaku:

            writer.writerow(elem)
            print(elem)
        
        else :
            print('被ってるよん')


driver.quit()
