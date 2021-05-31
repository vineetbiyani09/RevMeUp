from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(4)

link = 'https://www.flipkart.com'
url = ''
product_url = ''

driver.get(link)
driver.maximize_window()
time.sleep(1)

session = HTMLSession()

if driver.find_element(by = By.CLASS_NAME, value = '_3wFoIb') :
    driver.find_element(by = By.CLASS_NAME, value = '_2doB4z').click()
    time.sleep(1)

element = driver.find_element(by = By.CLASS_NAME, value = '_3704LK').send_keys('laptops')
search = driver.find_element(by = By.CLASS_NAME, value = '_34RNph').click()
time.sleep(1)

h_refs = []
csv_list = []

def link_scraper() :
    global h_refs

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    division = soup.findAll('div', {'class' : '_1YokD2 _3Mn1Gg'})
    divs = division[1].findAll('div', {'class' : '_13oc-S'})
    for div in divs :
        h_ref = div.find('a', {'class' : '_1fQZEK'}).get('href', None)
        h_refs.append(h_ref)
    time.sleep(1)

def data_scraper() :
    global h_refs
    global url
    global product_url
    global csv_list

    product_url = url
    response = session.get(url).text
    scraper_soup = BeautifulSoup(response, 'html.parser')
    division = scraper_soup.find('div', {'class' : 'aMaAEs'})
    product_name = division.find('span', {'class' : 'B_NuCI'}).text
    div = division.find('div', {'class' : 'dyC4hf'})
    offered_price = div.find('div', {'class' : '_30jeq3 _16Jk6d'}).text[1:]
    price = div.find('div', {'class' : '_3I9_wc _2p6lqe'})
    if price == None :
        original_price = offered_price
    else :
        original_price = price.text[1:]
    csv_list.append((product_name,original_price,offered_price,product_url))

file_name = 'main.csv'

x = 0
while x < 10 :
    link_scraper()
    pager = driver.find_element(by = By.CLASS_NAME, value = 'yFHi8N')
    inner_HTML = pager.get_attribute('innerHTML')
    soup1 = BeautifulSoup(inner_HTML, 'html.parser')
    tags = soup1.findAll('a', {'class' : '_1LKTO3'})
    if len(tags) == 2 and tags[1].text == 'Next' :
        element = driver.find_elements(by = By.CLASS_NAME, value = '_1LKTO3')
        element[1].click()
    elif len(tags) == 1 and tags[0].text == 'Next' :
        driver.find_element(by = By.CLASS_NAME, value = '_1LKTO3').click()
    x += 1

for h_ref in h_refs :
    url = link + h_ref
    data_scraper()

df = pd.DataFrame(csv_list, columns = ['Product_Name','Original_Price','Offered_Price','Product_Url'])
df.to_csv(file_name, index = False)

driver.quit()
