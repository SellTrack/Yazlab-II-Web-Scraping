import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages/beautifulsoup4-4.12.3')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import uuid
import re 
from bs4 import BeautifulSoup

import time
import subprocess

options = webdriver.ChromeOptions()
options.add_argument('headless')  # Run Chrome in headless mode, i.e., without opening a GUI window
options.add_argument('log-level=3')
driver_google = webdriver.Chrome(options=options)

def get_google_search_results(query):
    
    details = {}


    ignored_sites = ['facebook.com','twitter.com','instagram.com','linkedin.com','*.gov*'] # Sonuçlarda olmayacak.
    ignore = ""
    for site in ignored_sites:
        ignore += f" -site:{site}"
    url = "https://scholar.google.com/scholar?hl=tr&q=" + query + ignore
    driver_google.get(url)
    driver_google.implicitly_wait(3)
    
    


    # Captcha var mı diye kontrol eder.
    captcha = ""
    if(driver_google.current_url.find('google.com') > -1):
        try:
            captcha = driver_google.find_element(By.XPATH, "//iframe[contains(@src,'recaptcha')]") != -1
        except:
            captcha = ""
    else:
        captcha = ""
    
    # Captcha yoksa devam eder.
    while captcha != "":
        print("CAPTCHA tespit edildi. Lutfen cozun.")
        time.sleep(8)
        if(driver_google.current_url.find('google.com') > -1):
            try:
                captcha = driver_google.find_element(By.XPATH, "//iframe[contains(@src,'recaptcha')]") != -1
            except:
                captcha = ""
        else:
            captcha = ""
    else:
        
        soup = BeautifulSoup(driver_google.page_source, 'html.parser')
        search = soup.find_all('div', class_="gs_r gs_or gs_scl")
        results = []
        for h in search:
            details['url'] = h.find('h3', class_='gs_rt').find('a')['href']
            details['yayın id'] = str(uuid.uuid4())
            details['yayın adı'] = h.find('h3', class_='gs_rt').text
            details['yazar adı'] = h.find('div', class_='gs_a').text.split('-')[0].strip()
            details['yayın türü'] = ''
            details['yayınlanma tarihi'] = h.find('div', class_='gs_a').text.strip().split('-')[-2]
            publication_year = re.findall(r'\d{4}', details['yayınlanma tarihi'])[-1]
            details['yayınlanma tarihi'] = publication_year
            details['yayıncı adı'] = h.find('div', class_='gs_a').text.strip().split('-')[-2]
            publisher_name = re.findall(r'([^,]+)', details['yayıncı adı'])[0]
            details['yayıncı adı'] = publisher_name
            details['anahtar kelimeler (arama motorundan alınan)'] = query
            details['anahtar kelimeler (makaleye ait)'] = ''
            details['özet'] = h.find('div', class_='gs_rs').text
            details['referanslar'] = ''
            details['alıntı sayısı'] = h.find('div', class_='gs_fl gs_flb').text.split(':')[1]
            details['doi numarası'] = ''
            print("\n------------------------------------------------CIKAN SONUCLAR----------------------------------------\n")
            print("url adresi : ", details['url'], "\n")
            print("yayın id : ", details['yayın id'], "\n")
            print("yayın adı : ", details['yayın adı'], "\n")
            print("yayın türü : ", details['yayın türü'], "\n")
            print("yayınlanma tarihi : ", details['yayınlanma tarihi'], "\n")
            print("yayıncı adı : ", details['yayıncı adı'], "\n")
            print("anahtar kelimeler (arama motorundan alınan) : ", details['anahtar kelimeler (arama motorundan alınan)'], "\n")
            print("anahtar kelimeler (makaleye ait) : ", details['anahtar kelimeler (makaleye ait)'], "\n")
            print("özet : ", details['özet'], "\n")
            print("referanslar : ", details['referanslar'], "\n")
            print("alıntı numarası : ", details['alıntı sayısı'], "\n")
            print("doi numarası : ", details['doi numarası'], "\n")
            print("\n----------------------------------------------------------------------------------------------------\n")
            results.append(details)


    #return results 



args_as_string = ' '.join(sys.argv[1:])
print(get_google_search_results(args_as_string.strip("'")))
# Ornek kullanim: "dosyaadi.py 'aranacak konu'"


print("**BITTI**")