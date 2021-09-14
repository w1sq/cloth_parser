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

urls = ['https://www.saksoff5th.com/on/demandware.store/Sites-SaksOff5th-Site/en_US/Search-UpdateGrid?cgid=1549042144829&prefn1=brand&prefv1=Ash|Australia%20Luxe%20Collective|Calvin%20Klein%20Jeans|Karl%20Lagerfeld%20Paris|KENZO|Michael%20Kors|MICHAEL%20Michael%20Kors|Steve%20Madden|Tommy%20Hilfiger|UGG&srule=featured_newest&start=0&sz=24&filter=true&selectedUrl=https%3A%2F%2Fwww.saksoff5th.com%2Fon%2Fdemandware.store%2FSites-SaksOff5th-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3D1549042144829%26prefn1%3Dbrand%26prefv1%3DAsh%257cAustralia%2520Luxe%2520Collective%257cCalvin%2520Klein%2520Jeans%257cKarl%2520Lagerfeld%2520Paris%257cKENZO%257cMichael%2520Kors%257cMICHAEL%2520Michael%2520Kors%257cSteve%2520Madden%257cTommy%2520Hilfiger%257cUGG%26srule%3Dfeatured_newest%26start%3D72%26sz%3D24%26filter%3Dtrue&showMore=true',
'https://www.saksoff5th.com/c/women/apparel/armani-jeans_boss-hugo-boss_calvin-klein_calvin-klein-jeans_calvin-klein-performance_ck-jeans_dkny_dkny-sport_guess_karl-lagerfeld_karl-lagerfeld-paris_kenzo1_lacoste_loro-piana_michael-kors_michael-michael-kors_msgm_ralph-lauren_tommy-hilfiger_tommy-hilfiger-sport?srule=featured_newest']
url = 'https://www.saksoff5th.com'

chrome_options = Options()
chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4147.125 Safari/537.36")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
browser.implicitly_wait(5)

def main(main_link):
    browser.get(main_link)
            
loop = asyncio.get_event_loop()
if __name__ == '__main__':
    while True:
        for link in urls:
            main(link)
        print('finished')
        sleep(60)