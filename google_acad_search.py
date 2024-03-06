from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import time
import subprocess

import sys

options = webdriver.ChromeOptions()
options.add_argument('headless')  # Run Chrome in headless mode, i.e., without opening a GUI window
options.add_argument('log-level=3')
driver_google = webdriver.Chrome(options=options)

def get_google_search_results(query):

    ignored_sites = ['facebook.com','twitter.com','instagram.com','linkedin.com','*.gov*'] # Sonuçlarda olmayacak.
    ignore = ""
    for site in ignored_sites:
        ignore += f" -site:{site}"
    url = "https://scholar.google.com/scholar?hl=tr&q=" + query + ignore
    driver_google.get(url)
    driver_google.implicitly_wait(2)

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
            results.append(h.a.get('href'))

        # Sonuçlarda istenmeyen siteleri siler.
        # ignored_sites = ['facebook','twitter','instagram','linkedin','.gov']
        # results = [item for item in results if not any(banned_word in item for banned_word in ignored_sites)]

        # Sadece websiteyi alır. 
        # for i, site1 in enumerate(results):
        #    results[i] = site1[:site1.find('/', 8)+1] # Temiz urlyi alır.
        results = list(set(results))    # Kopyaları siler.

        # Yarı otomatik yöntem. Mail aranacak siteyi seçmemiz için bekliyor.
        time.sleep(4)

    return results 

args_as_string = ' '.join(sys.argv[1:])
print(get_google_search_results(args_as_string.strip("'")))
# Ornek kullanim: "dosyaadi.py 'aranacak konu'"
print("**BITTI**")