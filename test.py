import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')  
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages/beautifulsoup4-4.12.3')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import uuid
import re 
import subprocess
import os
import random
import requests
from shutil import move
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
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

def pdf_indir_ve_tasi(pdf_url, hedef_klasor):
    
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # İstek başarısız olursa hata fırlat

      # PDF dosyasını indirilenler klasörüne kaydet
              # Tarih ve saat bilgisini al
        tarih_saat = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        
        # Dosya adını oluştur ve boşlukları alt çizgi ile değiştir
        hedef_dosya = f"{tarih_saat}.pdf"

        rastgele_sayi = random.randint(1000, 9999)
        hedef_dosya = f"{tarih_saat}_{rastgele_sayi}.pdf"
        
        # Dosya adını oluştur ve boşlukları alt çizgi ile değiştir
        hedef_dosya = hedef_dosya.replace("/", ":")
        hedef_dosya = hedef_dosya.replace("_", " ")
        
        indirilen_dosya_yolu = os.path.join(hedef_klasor, hedef_dosya)

        
        with open(indirilen_dosya_yolu, 'wb') as dosya:
            dosya.write(response.content)

        print(f"{indirilen_dosya_yolu} başarıyla indirildi.")

        # PDF dosyasını hedef klasöre taşı
        hedef_klasor_yolu = os.path.join(os.getcwd(), hedef_klasor)
        tasinan_dosya_yolu = os.path.join(hedef_klasor_yolu, hedef_dosya)
       
        move(indirilen_dosya_yolu, tasinan_dosya_yolu)
        print(f"{hedef_klasor_yolu} klasörüne taşındı.")
        
    except requests.exceptions.RequestException as hata:
        print(f"Hata oluştu: {hata}")
    return

args_as_string = ' '.join(sys.argv[1:])
pdf_links = get_google_search_results(args_as_string.strip("'"))

hedef_klasor = "downloaded-files"
for pdf_link in pdf_links:
    pdf_indir_ve_tasi(pdf_link, hedef_klasor)

print("**BITTI**")
