from tkinter import Tk

import requests
from aiogram import Bot
from aiogram.types import ParseMode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.config import BOT_TOKEN, chat_id
from data.dbhandler import get_user, add_user


async def parsing():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-infobars")
    browser = webdriver.Chrome('chromedriver', chrome_options=option)
    browser.maximize_window()
    browser.get('https://opensea.io/activity?search[eventTypes][0]=AUCTION_CREATED')
    soup = BeautifulSoup(browser.page_source, "html.parser")
    elements = soup.find_all("div", attrs={"role" : "listitem"})
    for element in elements:
        links_list = []
        hasTwitter = False
        link = element.find_all_next("a")[2].get('href')
        print(link)
        # link = '/NFTKingCreator'
        # link = '/supercrypto571'
        # link = '/BigShibaDoge'
        # link = '/ZombieApeSurvival'
        browser.get('https://opensea.io' + link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        div = soup.find_all("div", class_='fresnel-container')
        if len(div) >= 2:
            links = div[1].find_all_next("a")
        # links = soup.find_all("a")
            for link in links:
                if link.get('href') != None:
                    if str(link.get('href')).startswith("https://instagram.com/") or str(link.get('href')).startswith("https://twitter.com/"):
                        print(link.get('href'))
                        hasTwitter = True
                        links_list.append(link.get('href'))

        if hasTwitter:
            hasAddress = False
            div = soup.find_all("div", class_='fresnel-container')
            btns = div[3].find_all_next("button")
            print(len(btns))
            btn = div[3].find_all_next("button")[6]
            print(btn)
            if btn.get('aria-label') == None and btn.get('aria-controls')== None:
                class__ = btn.get("class")[1]
                browser.find_element(By.CLASS_NAME, class__).click()
                tk = Tk()
                link = tk.clipboard_get()
                print(link)
                addesss = link
                hasAddress = True
                tk.quit()
            else:
                if btn.get('aria-controls') == None:
                    btn = div[3].find_next("div").find_all_next("div")[16].find_all_next("div")[31].find_all_next("button")[1]
                    class__ = btn.get('class')[1]
                    btns = browser.find_elements(By.CLASS_NAME, class__)
                    if len(btns) == 1:
                        btns[0].click()
                    else:
                        btns[3].click()

                    try:
                        links = browser.find_element(By.CLASS_NAME, "tippy-content")
                        if len(links.find_elements(By.TAG_NAME, "li")) > 0:
                            if len(links.find_elements(By.TAG_NAME, "li")) > 1:
                                links.find_elements(By.TAG_NAME, "li")[1].click()
                            else:
                                links.find_elements(By.TAG_NAME, "li")[0].click()
                        tk = Tk()
                        link = tk.clipboard_get()
                        print(link)
                        addesss = link
                        hasAddress = True
                        tk.quit()
                    except:
                        hasAddress = False
                        continue
                else:
                    continue

            if hasAddress:
                if get_user(user_id=addesss) != None:
                    continue
                url = 'https://debank.com/profile/' + addesss
                browser.get(url)
                elem = WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "db-user-avatar-container")))
                soup = BeautifulSoup(browser.page_source, "html.parser")
                # print(soup)
                # browser.save_screenshot("gg.png")
                balance = soup.find_all("div", class_=lambda value: value and value.startswith("HeaderInfo_totalAssetInner"))[0].text
                if int(balance[1:]) > 0:
                    await bot.send_message(chat_id=chat_id, text=f"<code>{addesss}</code>\n"
                                                           f"{links_list}\n"
                                                           f"{balance}\n", disable_web_page_preview=True)
                    add_user(user_id=addesss, twitter=" ".join(links_list))

        # break
    browser.close()

