import asyncio
import requests
from bs4 import BeautifulSoup
import lxml
from aiohttp import ClientSession
from multiprocessing.pool import ThreadPool
from time import sleep
import csv
from shutil import copyfile
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }

urls = ['https://www.macys.com/shop/sale/Brand,Business_category/A%257CX%20Armani%20Exchange%7CArmani%20Exchange%7CCalvin%20Klein%7CCalvin%20Klein%20Jeans%7CCOACH%7CDKNY%7CDKNY%20Jeans%7CEmporio%20Armani%7CGUESS%7CHUGO%7CHugo%20Boss%7CKarl%20Lagerfeld%7CKarl%20Lagerfeld%20Paris%7CLacoste%7CLevi%27s%7CMarc%20Jacobs%7CMichael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20by%20Ralph%20Lauren%7CRalph%20Lauren%7CSteve%20Madden%7CTommy%20Hilfiger%7CTommy%20Jeans%7CUGG%C2%AE,Handbags%20%26%20Accessories%7CKids%20%26%20Baby%7CMen%7CMen%27s%20Shoes%7CWomen%7CWomen%27s%20Shoes?id=3536'
,'https://www.saksoff5th.com/c/shoes/ash_australia-luxe-collective_calvin-klein-jeans_karl-lagerfeld-paris_kenzo1_michael-kors_michael-michael-kors_steve-madden_tommy-hilfiger_ugg?srule=featured_newest'
,'https://www.saksoff5th.com/c/women/apparel/armani-jeans_boss-hugo-boss_calvin-klein_calvin-klein-jeans_calvin-klein-performance_ck-jeans_dkny_dkny-sport_guess_karl-lagerfeld_karl-lagerfeld-paris_kenzo1_lacoste_loro-piana_michael-kors_michael-michael-kors_msgm_ralph-lauren_tommy-hilfiger_tommy-hilfiger-sport?srule=featured_newest'
,'https://www.saksoff5th.com/c/handbags/coach1_furla_karl-lagerfeld-paris_marc-jacobs_zac-zac-posen?srule=featured_newest'
,'https://usa.tommy.com/en/tommy-hilfiger-sale'
,'https://www.bloomingdales.com/shop/sale/sale-and-clearance/Brand/Armani%7CAsh%7CCalvin%20Klein%7CCOACH%7CDKNY%7CKARL%20LAGERFELD%20PARIS%7CKenzo%7CLacoste%7CMARC%20JACOBS%7CMichael%20Kors%7CMICHAEL%20Michael%20Kors%7CPolo%20Ralph%20Lauren%7CRalph%20Lauren%7CUGG%C2%AE?id=1003304'
,'https://www.michaelkors.com/sale/view-all-sale/_/N-28zn'
,'https://www.donnakaran.com/category/dkny/sale/womens+sale+view+all.do'
,'https://www.donnakaran.com/category/dkny/sale/mens+sale+view+all.do'
,'https://www.nordstromrack.com/shop/Women/Clothing?breadcrumb=Home%2FWomen%2FClothing&origin=topnav&filterByBrand=calvin-klein&filterByBrand=dkny&filterByBrand=guess&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=tommy-hilfiger'
,'https://www.nordstromrack.com/shop/Women/Shoes?breadcrumb=Home%2FShoes%2FWomen%27s%20Shoes&origin=topnav&filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=dkny&filterByBrand=dr-martens&filterByBrand=dr-martens&filterByBrand=karl-lagerfeld-paris&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=steve-madden&filterByBrand=timberland&filterByBrand=tommy-hilfiger&filterByBrand=ugg'
,'https://www.nordstromrack.com/shop/women/handbags?filterByBrand=calvin-klein&filterByBrand=coach&filterByBrand=coach&filterByBrand=coccinelle&filterByBrand=dkny&filterByBrand=karl-lagerfeld-paris&filterByBrand=marc-by-marc-jacobs&filterByBrand=marc-jacobs&filterByBrand=michael-kors&filterByBrand=michael-michael-kors&filterByBrand=moschino&filterByBrand=tommy-hilfiger']

urls = ['https://www.saksoff5th.com/c/shoes/ash_australia-luxe-collective_calvin-klein-jeans_karl-lagerfeld-paris_kenzo1_michael-kors_michael-michael-kors_steve-madden_tommy-hilfiger_ugg?srule=featured_newest'
,'https://www.saksoff5th.com/c/women/apparel/armani-jeans_boss-hugo-boss_calvin-klein_calvin-klein-jeans_calvin-klein-performance_ck-jeans_dkny_dkny-sport_guess_karl-lagerfeld_karl-lagerfeld-paris_kenzo1_lacoste_loro-piana_michael-kors_michael-michael-kors_msgm_ralph-lauren_tommy-hilfiger_tommy-hilfiger-sport?srule=featured_newest'
,'https://www.saksoff5th.com/c/handbags/coach1_furla_karl-lagerfeld-paris_marc-jacobs_zac-zac-posen?srule=featured_newest'
,'https://usa.tommy.com/en/tommy-hilfiger-sale']

chrome_options = Options()
chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4147.125 Safari/537.36")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
browser.implicitly_wait(5)

def saksoff(main_link):
    browser.get(main_link)
    update_link ='https://www.saksoff5th.com/on/demandware.store/Sites-SaksOff5th-Site/en_US/Search-UpdateGrid?'
    count = int(browser.find_element_by_class_name('search-count').get_attribute('data-search-count'))
    all_data_link=browser.find_element_by_xpath('//div[@data-action="Search-Show"]').get_attribute('data-querystring')
    start = 0
    with open('test.txt','w') as f:
        while start < count:
            browser.get(update_link+all_data_link+f'&start={start}')
            namesandlinks = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//a[@class="link"]')
            prices = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//span[@class="prod-price"]')
            image_blocks = browser.find_elements_by_xpath('//div[@class="col-6 col-sm-4 col-xl-3"]//div[@class="image-container"]//a[@class="thumb-link"]')
            for i in range(len(namesandlinks)):
                f.write(prices[i*2].text+'\n')
                f.write(namesandlinks[i].text+'\n')
                f.write(namesandlinks[i].get_attribute('href')+'\n')
                f.write(image_blocks[i].find_element_by_class_name('tile-image').get_attribute('src')+'\n\n')
            start += len(namesandlinks)

def tommy(main_link):
    browser.get(main_link)
    button = browser.find_elements_by_xpath('//div[@class="pvhOverlayCloseX"]')
    if button:
        button[0].click()
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    img_links = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//span[@itemprop='url']")
    links = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//span[@itemprop='image']")
    names = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//div[contains(@class,'productInfo')]//div[@class='productName']")
    prices = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//div[contains(@class,'productInfo')]//div[@class='productPrice ']//div[@id='price_display']//span")
    msg = browser.find_elements_by_xpath("//div[contains(@class,'productCell processed')]//div[contains(@class,'productInfo')]//div[contains(@class,'promoMessage')]//span")
    with open('tommy.txt','w') as f:
        for i in range(len(names)):
            img_link = img_links[i].get_attribute('content')
            name = names[i].text
            img_link = links[i].get_attribute('content')
            print(name,img_link)
            print(link)
            price = prices[i*2].text+prices[i*2+1].text
            all_message = msg[i].text+'\n'+price
            print(all_message)
            f.write(name+'\n'+link+'\n'+img_link+'\n'+all_message+'\n\n')

def michael(main_link):
    pass

def macys(main_link):
    pass

def bloomingdales(main_link):
    pass

def nordstromrack(main_link):
    pass
    
def donnakaran(main_link):
    pass


funcs = {
    'https://www.saksoff5th':saksoff,
    'https://www.michaelkors':michael,
    'https://www.macys':macys,
    'https://usa.tommy':tommy,
    'https://www.bloomingdales':bloomingdales,
    'https://www.donnakaran':donnakaran,
    'https://www.nordstromrack':nordstromrack
}

loop = asyncio.get_event_loop()
if __name__ == '__main__':
    while True:
        for link in urls:
            funcs[link.split('.com')[0]](link)
        print('finished')
        sleep(60)