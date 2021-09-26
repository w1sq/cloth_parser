# coding=utf8
import asyncio
from asyncio import events
import logging
import aiogram.utils.markdown as fmt
from datetime import datetime
from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputTextMessageContent, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types.bot_command import BotCommand
from aiogram.types.inline_query_result import InlineQueryResultArticle
from sqlite3 import IntegrityError
from db_data import db_session
from db_data.__all_models import Users
import asyncio
from multiprocessing.pool import ThreadPool
from time import sleep
import json 
import csv
from shutil import copyfile
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }
urls = ['https://www.macys.com/shop/sale/Brand,Business_category,Pageindex,Productsperpage/A%257CX%20Armani%20Exchange%7CArmani%20Exchange%7CCalvin%20Klein%7CCalvin%20Klein%20Jeans%7CCOACH%7CDKNY%7CDKNY%20Jeans%7CEmporio%20Armani%7CGUESS%7CHUGO%7CHugo%20Boss%7CKarl%20Lagerfeld%7CKarl%20Lagerfeld%20Paris%7CLacoste%7CLevi%27s%7CMarc%20Jacobs%7CMichael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20by%20Ralph%20Lauren%7CRalph%20Lauren%7CSteve%20Madden%7CTommy%20Hilfiger%7CTommy%20Jeans%7CUGG%C2%AE,Handbags%20%26%20Accessories%7CKids%20%26%20Baby%7CMen%7CMen%27s%20Shoes%7CWomen%7CWomen%27s%20Shoes.120,1,120?id=3536'
,'https://www.saksoff5th.com/c/shoes/ash_australia-luxe-collective_calvin-klein-jeans_karl-lagerfeld-paris_kenzo1_michael-kors_michael-michael-kors_steve-madden_tommy-hilfiger_ugg?srule=featured_newest'
,'https://www.saksoff5th.com/c/women/apparel/armani-jeans_boss-hugo-boss_calvin-klein_calvin-klein-jeans_calvin-klein-performance_ck-jeans_dkny_dkny-sport_guess_karl-lagerfeld_karl-lagerfeld-paris_kenzo1_lacoste_loro-piana_michael-kors_michael-michael-kors_msgm_ralph-lauren_tommy-hilfiger_tommy-hilfiger-sport?srule=featured_newest'
,'https://www.saksoff5th.com/c/handbags/coach1_furla_karl-lagerfeld-paris_marc-jacobs_zac-zac-posen?srule=featured_newest'
,'https://usa.tommy.com/en/tommy-hilfiger-sale'
,'https://www.bloomingdales.com/shop/sale/sale-and-clearance/Brand/Armani%7CAsh%7CCalvin%20Klein%7CCOACH%7CDKNY%7CKARL%20LAGERFELD%20PARIS%7CKenzo%7CLacoste%7CMARC%20JACOBS%7CMichael%20Kors%7CMICHAEL%20Michael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20Lauren%7CUGG%C2%AE?id=1003304'
,'https://www.michaelkors.com/sale/view-all-sale/_/N-28zn'
,'https://www.donnakaran.com/category/dkny/sale/womens+sale+view+all.do?page=all'
,'https://www.donnakaran.com/category/dkny/sale/mens+sale+view+all.do?page=all'
,'https://www.nordstromrack.com/shop/Women/Clothing?breadcrumb=Home%2FWomen%2FClothing&origin=topnav&filterByBrand=calvin-klein&filterByBrand=dkny&filterByBrand=guess&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=tommy-hilfiger'
,'https://www.nordstromrack.com/shop/Women/Shoes?breadcrumb=Home%2FShoes%2FWomen%27s%20Shoes&origin=topnav&filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=dkny&filterByBrand=dr-martens&filterByBrand=dr-martens&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=steve-madden&filterByBrand=timberland&filterByBrand=tommy-hilfiger&filterByBrand=ugg'
,'https://www.nordstromrack.com/shop/women/handbags?filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=coach&filterByBrand=coccinelle&filterByBrand=dkny&filterByBrand=karl-lagerfeld-paris&filterByBrand=marc-by-marc-jacobs&filterByBrand=marc-jacobs&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=tommy-hilfiger'
]
# urls = [
#     'https://www.bloomingdales.com/shop/sale/sale-and-clearance/Brand/Armani%7CAsh%7CCalvin%20Klein%7CCOACH%7CDKNY%7CKARL%20LAGERFELD%20PARIS%7CKenzo%7CLacoste%7CMARC%20JACOBS%7CMichael%20Kors%7CMICHAEL%20Michael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20Lauren%7CUGG%C2%AE?id=1003304'
# ,'https://www.michaelkors.com/sale/view-all-sale/_/N-28zn'
# ,'https://www.donnakaran.com/category/dkny/sale/womens+sale+view+all.do?page=all'
# ,'https://www.donnakaran.com/category/dkny/sale/mens+sale+view+all.do?page=all'
# ,'https://www.nordstromrack.com/shop/Women/Clothing?breadcrumb=Home%2FWomen%2FClothing&origin=topnav&filterByBrand=calvin-klein&filterByBrand=dkny&filterByBrand=guess&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=tommy-hilfiger'
# ,'https://www.nordstromrack.com/shop/Women/Shoes?breadcrumb=Home%2FShoes%2FWomen%27s%20Shoes&origin=topnav&filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=dkny&filterByBrand=dr-martens&filterByBrand=dr-martens&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=steve-madden&filterByBrand=timberland&filterByBrand=tommy-hilfiger&filterByBrand=ugg'
# ,'https://www.nordstromrack.com/shop/women/handbags?filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=coach&filterByBrand=coccinelle&filterByBrand=dkny&filterByBrand=karl-lagerfeld-paris&filterByBrand=marc-by-marc-jacobs&filterByBrand=marc-jacobs&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=tommy-hilfiger'
#  ]
numbers = ['1', '2','3','4','5','6','7','8','9','0']
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4147.125 Safari/537.36")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
browser.implicitly_wait(5)


def saksoff(main_link,id,response):
    browser.get(main_link)
    update_link ='https://www.saksoff5th.com/on/demandware.store/Sites-SaksOff5th-Site/en_US/Search-UpdateGrid?'
    count = int(browser.find_element_by_class_name('search-count').get_attribute('data-search-count'))
    all_data_link=browser.find_element_by_xpath('//div[@data-action="Search-Show"]').get_attribute('data-querystring')
    start = 0
    now_results = {}
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results =  json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        while start < count:
            browser.get(update_link+all_data_link+f'&start={start}')
            print(update_link+all_data_link+f'&start={start}')
            namesandlinks = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//a[@class="link"]')
            prices = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//span[@class="prod-price"]')
            image_blocks = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//div[@class="image-container"]//a[@class="thumb-link"]')
            for i in range(len(namesandlinks)):
                if len(prices[i*2].text.split()) == 8:
                    name= namesandlinks[i].text
                    img_link =image_blocks[i].find_element_by_class_name('tile-image').get_attribute('src')
                    all_price = prices[i*2].text
                    new_price = round(float(r(prices[i*2].text).split()[-3].replace('$','').replace(',','')),0)
                    product_link = namesandlinks[i].get_attribute('href')
                    if product_link in old_results.keys() and old_results[product_link]['new_price'] < new_price or product_link not in old_results.keys():
                        response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{product_link}")
                    now_results[namesandlinks[i].get_attribute('href')]={
                        'name':name,
                        'img_link':img_link,
                        'new_price':new_price,
                        'all_price':all_price
                    }
            start += 24
        json.dump(now_results,f)
    sleep(3)
    browser.refresh()


def tommy(main_link,id,response):
    browser.get(main_link)
    button = browser.find_elements_by_xpath('//div[@class="pvhOverlayCloseX"]')
    if button:
        button[0].click()
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    items_links = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//span[@itemprop='url']")
    img_links = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//span[@itemprop='image']")
    names = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//div[contains(@class,'productInfo')]//div[@class='productName']")
    prices = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//div[contains(@class,'productInfo')]//div[@class='productPrice ']//div[@id='price_display']")
    now_results = {}
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results =  json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        for i in range(len(names)):
            if len(r(prices[i].text).split()) == 1 and r(prices[i].text)[-1] in numbers and len(r(prices[i].text).split('$')) == 3:
                item_link = items_links[i].get_attribute('content')
                name = names[i].text
                img_link = img_links[i].get_attribute('content')
                new_price = round(float(r(prices[i].text).split('$')[2]),0)
                price = prices[i].text.split('$')[1]+' -> '+prices[i].text.split('$')[2]
                if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                    response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{price}\n{item_link}")
                now_results[item_link] = {
                    'name':name,
                    'img_link':img_link,
                    'new_price':new_price,
                    'all_price':price
                }
        json.dump(now_results,f)



def michael(main_link,id,response):
    def_prod_link = 'https://www.michaelkors.com'
    def_img_link = 'https://michaelkors.scene7.com/is/image/'
    n=1
    link = f'https://www.michaelkors.com/server/data/guidedSearch?stateIdentifier=_/N-28zn&No={n}&Nrpp=42'
    browser.get(link)
    jsondata = json.loads(browser.find_element_by_xpath('//pre').text)
    count=int(jsondata['result']['totalProducts'])
    now_results = {}
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results =  json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        while n<count:
            link = f'https://www.michaelkors.com/server/data/guidedSearch?stateIdentifier={main_link.split("view-all-sale/")[-1]}&No={n}&Nrpp=42'
            browser.get(link)
            jsondata = json.loads(browser.find_element_by_xpath('//pre').text)
            for product in jsondata['result']['productList']:
                item_link = def_prod_link + product['seoURL']
                img_link = def_img_link + product['media']['mediaSet']
                name = product['SKUs'][0]['name']
                old_price = round(float(product['prices']['highListPrice']),0)
                new_price = round(float(product['prices']['lowSalePrice']),0)
                if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                    response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{str(old_price)+'->'+str(new_price)}\n{item_link}")
                now_results[item_link]={
                    'name':name,
                    'img_link':img_link,
                    'new_price': new_price,
                    'all_price':str(old_price)+'->'+str(new_price)}
            n+= 42
        json.dump(now_results,f)



def macys(main_link,id,response):    
    n = 1
    link = f'https://www.macys.com/shop/sale/Brand,Business_category,Pageindex,Productsperpage/A%257CX%20Armani%20Exchange%7CArmani%20Exchange%7CCalvin%20Klein%7CCalvin%20Klein%20Jeans%7CCOACH%7CDKNY%7CDKNY%20Jeans%7CEmporio%20Armani%7CGUESS%7CHUGO%7CHugo%20Boss%7CKarl%20Lagerfeld%7CKarl%20Lagerfeld%20Paris%7CLacoste%7CLevi%27s%7CMarc%20Jacobs%7CMichael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20by%20Ralph%20Lauren%7CRalph%20Lauren%7CSteve%20Madden%7CTommy%20Hilfiger%7CTommy%20Jeans%7CUGG%C2%AE,Handbags%20%26%20Accessories%7CKids%20%26%20Baby%7CMen%7CMen%27s%20Shoes%7CWomen%7CWomen%27s%20Shoes.120,{n},120?id=3536'
    browser.get(link)
    selection = len(browser.find_elements_by_xpath("//div[@id='filterResultsBottom']//ul[@class='filters']//li[@class='pagination']//ul[@class='pagePagination']//li//select[@id='select-page']//option"))
    if selection:
        now_results = {}
        with open(str(id)+'.json','r') as f:
            data = f.read()
            if data:
                old_results =  json.loads(data)
            else:
                old_results = {}
        with open(str(id)+'.json','w') as f:
            while n<selection:
                link = f'https://www.macys.com/shop/sale/Brand,Business_category,Pageindex,Productsperpage/A%257CX%20Armani%20Exchange%7CArmani%20Exchange%7CCalvin%20Klein%7CCalvin%20Klein%20Jeans%7CCOACH%7CDKNY%7CDKNY%20Jeans%7CEmporio%20Armani%7CGUESS%7CHUGO%7CHugo%20Boss%7CKarl%20Lagerfeld%7CKarl%20Lagerfeld%20Paris%7CLacoste%7CLevi%27s%7CMarc%20Jacobs%7CMichael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20by%20Ralph%20Lauren%7CRalph%20Lauren%7CSteve%20Madden%7CTommy%20Hilfiger%7CTommy%20Jeans%7CUGG%C2%AE,Handbags%20%26%20Accessories%7CKids%20%26%20Baby%7CMen%7CMen%27s%20Shoes%7CWomen%7CWomen%27s%20Shoes.120,{n},120?id=3536'
                browser.get(link)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                all_imgs = browser.find_elements_by_xpath("//div[@class='cell']//ul[contains(@class,'items')]//li[contains(@class,'cell productThumbnailItem')]//div[contains(@class,'productThumbnail')]//div[contains(@class,'productThumbnailImage')]//a//div//picture//img")
                all_names_and_links = browser.find_elements_by_xpath("//div[@class='cell']//ul[contains(@class,'items')]//li[contains(@class,'cell productThumbnailItem')]//div[contains(@class,'productThumbnail')]//div[contains(@class,'productDetail')]//div[contains(@class,'productDescription')]//a[contains(@class,'productDescLink')]")
                all_prices = browser.find_elements_by_xpath("//div[@class='cell']//ul[contains(@class,'items')]//li[contains(@class,'cell productThumbnailItem')]//div[contains(@class,'productThumbnail')]//div[contains(@class,'productDetail')]//div[contains(@class,'productDescription')]//div[contains(@class,'priceInfo')]//div[contains(@class,'prices')]")
                for i in range(len(all_names_and_links)):
                    if len(r(all_prices[i].text).split()) == 3:
                        name = r(all_names_and_links[i].text)
                        item_link = all_names_and_links[i].get_attribute('href')
                        img_link = all_imgs[i].get_attribute('src')
                        new_price = round(float(r(all_prices[i].text).split()[-1].replace('$','')),0)
                        all_price = r(all_prices[i].text)
                        if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                            response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{item_link}")
                        now_results[item_link]={
                            'name':name,
                            'img_link':img_link,
                            'new_price':new_price,
                            'all_price':all_price
                        }
                n+=1
            json.dump(now_results,f)

        



def bloomingdales(main_link,id,response):
    n = 1
    link = f'https://www.bloomingdales.com/shop/sale/sale-and-clearance/Brand,Pageindex/Armani|Ash|Calvin%20Klein|COACH|DKNY|KARL%20LAGERFELD%20PARIS|Kenzo|Lacoste|MARC%20JACOBS|Michael%20Kors|MICHAEL%20Michael%20Kors|Polo%20Ralph%20Lauren|Ralph%20Lauren|UGG%C2%AE,{n}?id=1003304'
    browser.get(link)
    selection = len(browser.find_elements_by_xpath("//div[@id='filterBottom']//div[@class='paginationBottom']//ul[@class='newPagination']//li[@class='paginateContainer']//div[contains(@class,'sort-pagination')]//select[@id='sort-pagination-select-bottom']//option"))
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results = json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        while n<selection:
            link = f'https://www.bloomingdales.com/shop/sale/sale-and-clearance/Brand,Pageindex/Armani|Ash|Calvin%20Klein|COACH|DKNY|KARL%20LAGERFELD%20PARIS|Kenzo|Lacoste|MARC%20JACOBS|Michael%20Kors|MICHAEL%20Michael%20Kors|Polo%20Ralph%20Lauren|Ralph%20Lauren|UGG%C2%AE,{n}?id=1003304'
            browser.get(link)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            all_imgs = browser.find_elements_by_xpath("//div[contains(@class,'sortableGrid')]//ul[contains(@class,'items')]//li[contains(@class,'cell')]//div[contains(@class,'productThumbnail')]//a[contains(@class,'productDescLink')]//div[contains(@class,'productThumbnailImage')]//div[contains(@class,'thumbnailImageContainer')]//picture[contains(@class,'primary-image')]//img[contains(@class,'thumbnailImage')]")
            all_names = browser.find_elements_by_xpath("//div[contains(@class,'sortableGrid')]//ul[contains(@class,'items')]//li[contains(@class,'cell')]//div[contains(@class,'productThumbnail')]//a[contains(@class,'productDescLink')]//div[contains(@class,'productDescription')]")
            all_links = browser.find_elements_by_xpath("//div[contains(@class,'sortableGrid')]//ul[contains(@class,'items')]//li[contains(@class,'cell')]//div[contains(@class,'productThumbnail')]//a[contains(@class,'productDescLink')]")
            all_prices = browser.find_elements_by_xpath("//div[contains(@class,'sortableGrid')]//ul[contains(@class,'items')]//li[contains(@class,'cell')]//div[contains(@class,'productThumbnail')]//div[contains(@class,'productDetail')]//div[contains(@class,'priceInfo')]")
            for i in range(len(all_names)):
                name = r(all_names[i].text)
                new_price = round(float(r(all_prices[i].text).split()[2].replace('$','').replace(',','')),0)
                all_price = r(all_prices[i].text)
                item_link = all_links[i].get_attribute('href')
                if i < 6:
                    if len(r(all_prices[i].text).split()) == 5 and r(all_prices[i].text).endswith('OFF)'):
                        img_link = all_imgs[i].get_attribute('src')
                        if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                            response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{item_link}")
                        now_results[item_link] = {
                            'name': name,
                            'img_link':img_link,
                            'new_price':new_price,
                            'all_price':all_price
                            }
                else:
                    if len(r(all_prices[i].text).split()) == 5 and r(all_prices[i].text).endswith('OFF)'):
                        img_link = all_imgs[i].get_attribute('data-lazysrc')
                        if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                            response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{item_link}")
                        now_results[item_link] = {
                            'name': name,
                            'img_link':img_link,
                            'new_price':new_price,
                            'all_price':all_price
                            }
            n+=1
        json.dump(now_results,f)


def nordstromrack(main_link,id,response):
    n = 1
    link = main_link + f'&page={n}'
    browser.get(link)
    sleep(3)
    browser.refresh()
    number = float(browser.find_element_by_xpath("//div[@id='product-results-view']//header//span[contains(.,'items')]").text.split()[0])
    count = 0
    now_results = {}
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results =  json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        while count < number:
            link = main_link + f'&page={n}'
            browser.get(link)
            sleep(3)
            browser.refresh()
            all_imgs = browser.find_elements_by_xpath("//div[@id='product-results-view']//div//div//div//section//div//article//div[1]//img")
            all_names = browser.find_elements_by_xpath("//div[@id='product-results-view']//div//div//div//section//div//article//h3")
            all_prices = browser.find_elements_by_xpath("//div[@id='product-results-view']//div//div//div//section//div//article//div[contains(@class,'_2NEEx')]")
            all_new_prices = browser.find_elements_by_xpath("//div[@id='product-results-view']//div//div//div//section//div//article//div[contains(@class,'_2NEEx')]//div[1]")
            all_links = browser.find_elements_by_xpath("//div[@id='product-results-view']//div//div//div//section//div//article//a")
            for i in range(len(all_imgs)):
                name = all_names[i].text
                img_link = all_imgs[i].get_attribute('src')
                new_price = round(float(all_new_prices[i].text.split()[0].replace('$','')),0)
                all_price = all_prices[i].text.replace('\n',' ')
                item_link = all_links[i].get_attribute('href')
                if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                    response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{item_link}")
                now_results[item_link]={
                'name':name,
                'img_link':img_link,
                'new_price':new_price,
                'all_price':all_price
            }
            count += 72
            n+=1
        json.dump(now_results,f)
    

def donnakaran(main_link,id,response):
    browser.get(main_link)
    all_images = browser.find_elements_by_xpath("//div[contains(@class,'ml-directory')]//div[contains(@class,'ml-grid-view')]//div[contains(@id,'ml-grid-view-items')]//div[@role='group']//a//div[contains(@class,'ml-thumb-wrapper')]//div[contains(@class,'ml-grid-item-image')]//img")
    all_names_and_links = browser.find_elements_by_xpath("//div[contains(@class,'ml-directory')]//div[contains(@class,'ml-grid-view')]//div[contains(@id,'ml-grid-view-items')]//div[@role='group']//a")
    all_prices = browser.find_elements_by_xpath("//div[contains(@class,'ml-directory')]//div[contains(@class,'ml-grid-view')]//div[contains(@id,'ml-grid-view-items')]//div[@role='group']//a//div[contains(@class,'ml-thumb-wrapper')]//div[contains(@class,'ml-grid-item-info')]//div[contains(@class,'ml-thumb-price')]")
    now_results = {}
    now_results = {}
    with open(str(id)+'.json','r') as f:
        data = f.read()
        if data:
            old_results =  json.loads(data)
        else:
            old_results = {}
    with open(str(id)+'.json','w') as f:
        for i in range(len(all_names_and_links)):
            name = all_names_and_links[i].get_attribute('data-item-name')
            img_link = all_images[i].get_attribute('src')
            new_price = round(float(all_prices[i].text.split('\n')[-1].split()[-1].replace('$','')),0)
            all_price = all_prices[i].text.replace('\n',' ')
            item_link = all_names_and_links[i].get_attribute('href')
            if item_link in old_results.keys() and old_results[item_link]['new_price'] < new_price or item_link not in old_results.keys():
                response.append(f"<a href='{img_link}'>&#8205</a>\n{name}\n{all_price}\n{item_link}")
            now_results[item_link]={
                'name':name,
                'img_link':img_link,
                'new_price':new_price,
                'all_price':all_price
            }
        json.dump(now_results,f)

def r(string):
    return string.strip().replace('\n',' ')           

funcs = {
    'https://www.saksoff5th':saksoff,
    'https://www.michaelkors':michael,
    'https://www.macys':macys,
    'https://usa.tommy':tommy,
    'https://www.bloomingdales':bloomingdales,
    'https://www.donnakaran':donnakaran,
    'https://www.nordstromrack':nordstromrack
}

def main():
    response = []
    for i in range(len(urls)):
        funcs[urls[i].split('.com')[0]](urls[i],str(i),response)
    return response


with open('key.txt','r') as file:
    API_KEY = file.readline()
logging.basicConfig(level=logging.INFO, filename='botlogs.log')
bot = Bot(token=API_KEY)
storage = MemoryStorage()
db_session.global_init()
dp = Dispatcher(bot)
print('Bot started')

def generate_inline_keyboard (*answer):
    keyboard = InlineKeyboardMarkup()
    temp_buttons = []
    for i in answer:
        temp_buttons.append(InlineKeyboardButton(text=str(i[0]), callback_data=str(i[1])))
    keyboard.add(*temp_buttons)
    return keyboard


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота")
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['remove'])
async def remove(message):
    if message.chat.username == 'artem_kokorev':
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(Users).get(message.text.split()[-1])
        except Exception:
            await message.answer('Вы ввели неправильный тег пользователя, попробуйте снова')
            return
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
        await message.answer('Вы успешно удалили пользователя')

@dp.message_handler(commands=['list'])
async def return_list(message):
    if message.chat.id == 0:
        db_sess = db_session.create_session()
        users = db_sess.query(Users).all()
        string = ''
        for user in users:
            string += user.name+' '
        db_sess.close()
        if string != '':
            await message.answer(string)
        else:
            await message.answer('Нет пользователей')

@dp.message_handler(commands=['start'])
async def start(message):
    try:
        user_name = message.chat.username
    except Exception:
        await message.answer('Создайте уникальный nickname телеграма чтобы воспользоваться ботом.')
        return
    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(user_name)
    db_sess.close()
    if user:
        await message.answer(f'Добро пожаловать назад, {user_name}')
    else:
        await message.answer(f'Подожди пока тебя пустят')
        await bot.send_message('505248301', f'@{message.chat.username} хочет получить доступ к боту',reply_markup=generate_inline_keyboard(['Допустить',f'#pass {message.chat.id} {message.chat.username}']))
        
@dp.callback_query_handler(lambda call: True)
async def ans(call):
    message = call.message
    if call.data.startswith('#pass'):
        db_sess = db_session.create_session()
        user=Users(name=call.data.split()[2],telegram_id=call.data.split()[1])
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        await bot.send_message(call.data.split()[1],'Администратор подтвердил вас')

async def send(text):
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    db_sess.close()
    for user in users:
        await bot.send_message(user.telegram_id, text, parse_mode='html')

async def updation():
    while True:
        fresh_news = main()
        db_sess = db_session.create_session()
        users = db_sess.query(Users).all()
        db_sess.close()
        for user in users:
            for message in fresh_news:
                await bot.send_message(user.telegram_id, message, parse_mode='html')
        await asyncio.sleep(30*60)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(updation())
    executor.start_polling(dp)