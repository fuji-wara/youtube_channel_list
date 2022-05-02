from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from csv import DictWriter
import csv
import re


options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Selenium サーバーへ接続する。
driver = webdriver.Remote(

    command_executor=os.environ["SELENIUM_URL"],
    desired_capabilities=options.to_capabilities(),
    options=options,

)
two_months_ago = "2022/2/10"
base_url = 'https://www.youtube.com'
labels = ['チャンネル名', 'チャンネルURL', '投稿頻度', '最新動画投稿日', '動画本数']
channel_list = 'ccv_dict2.csv'
cannnel_researched ='チャンネルリサーチ除外一覧表 - リサーチ除外一覧表.csv'
cahnnel_register ='登録できるチャンネル.csv'


def main():

    comparison = hikaku_list()

    with open(channel_list, 'r') as ff:
        reader = csv.DictReader(ff)
        l = [row for row in reader]

    for i in l:
        channel_title = i['name']
        channel_url = i['url']
        channel_all = i['vido']
        channel_dict = scrap_cannel(channel_title, channel_url, channel_all, comparison)

        with open(cahnnel_register, 'a', newline='') as fff:
            writer = DictWriter(fff, fieldnames=labels)
            writer.writerow(channel_dict)


def hikaku_list():
    """
    リサーチ済みチャンネル名をリストにする。
    """
    hikaku = [] 
    with open(cannnel_researched, 'r') as f:
        reader = csv.DictReader(f)
        z = [row for row in reader]

    for x in z:
        c = x['チャンネル名']
        hikaku.append(c)
    
    return hikaku


def scrap_cannel(channel_title, channel_url, channel_all, comparison):
    """
    リサーチ済み、最新動画が二ヶ月前か確認して辞書作成。
    """

    if channel_title not in comparison:
        driver.get(f'{channel_url}/videos')
        time.sleep(5)
        html1 = driver.page_source.encode('utf-8')
        soup1 = BeautifulSoup(html1, 'lxml')
        
        z = soup1.select_one('a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail').get('href') 
        latest_day_url =f'{base_url}{z}'

        driver.get(latest_day_url)
        time.sleep(10)
        html2 = driver.page_source.encode('utf-8')
        soup2 = BeautifulSoup(html2, 'lxml')
        pattern = r'\b\d{4}/\d{2}/\d{2}\b'
        try:
            try: # 通常動画
                day = soup2.find(id="info-strings" ).find("yt-formatted-string", class_="style-scope ytd-video-primary-info-renderer").text
                day = re.search(pattern, day).group()

            except: # ショート動画
                driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[1]/ytd-reel-video-renderer[1]/div[2]/ytd-reel-player-overlay-renderer/div[2]/div[1]/ytd-menu-renderer/yt-icon-button/button/yt-icon').click()
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-icon').click()
                time.sleep(5)
                element = driver.find_elements_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-reel-description-sheet-renderer/div[2]/div/yt-formatted-string/span[1]')
                time.sleep(2)
                day = element[0].text
                day = re.search(pattern, day).group()
    
        except:
            print('sippai')
            day  = ''
            channel_dict = {'チャンネル名': channel_title, 'チャンネルURL': channel_url, '投稿頻度':'', '最新動画投稿日':latest_day, '動画本数': all_vidos}
            return channel_dict

        latest_day = day
        print(latest_day)

        first_data = latest_day
        second_data = two_months_ago

        format1 = time.strptime(first_data, "%Y/%m/%d")
        format2 = time.strptime(second_data, "%Y/%m/%d")
        if format1 > format2 :

            all_vidos = re.sub(r"\D", "", channel_all) # 正規表現で数字のみ取得
            channel_dict = {'チャンネル名': channel_title, 'チャンネルURL': channel_url, '投稿頻度':'', '最新動画投稿日':latest_day, '動画本数': all_vidos}
            return channel_dict
        else:
            print('二ヶ月更新なし')
    
    else:
        print('被ってる')