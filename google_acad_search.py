import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages/beautifulsoup4-4.12.3')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import uuid
import random
import requests
import time 
import re 
from datetime import datetime
import pdfdownload
from bs4 import BeautifulSoup

import time
import subprocess

download_folder = os.path.join(os.getcwd(), 'downloaded-files')

options = webdriver.ChromeOptions()
options.add_argument('headless')  # Run Chrome in headless mode, i.e., without opening a GUI window
prefs = {"download.default_directory": "downloaded_files"}
options.add_experimental_option('prefs', prefs)
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

# Sonuçları yazdır


def indir_ve_kaydet(pdf_url, hedef_klasor):
    try:
        # PDF dosyasını indir
        response = requests.get(pdf_url)
        response.raise_for_status()  # Hata kontrolü
        
        # Rastgele bir sayı oluştur (benzersiz dosya adı için)
        rastgele_sayi = random.randint(1000, 9999)

        # PDF dosyasının adını oluştur
        dosya_adi = f"{rastgele_sayi}.pdf"
        
        # Dosya yolu oluştur
        dosya_yolu = os.path.join(hedef_klasor, dosya_adi)
        
        # PDF dosyasını kaydet
        with open(dosya_yolu, 'wb') as dosya:
            dosya.write(response.content)
        
        print(f"{dosya_yolu} başarıyla indirildi.")
    
    except requests.exceptions.RequestException as hata:
        print(f"Hata oluştu: {hata}")


def get_google_search_results(query):
    
    details = {}
    url = f"https://dergipark.org.tr/tr/search?q={query}&section=articles"
    driver.get(url)
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL+Keys.END)    
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_="card article-card dp-card-outline")
    results = []
    for h in range(len(search)):
        h += 1
        try:
            parent = "/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[{h}]"
            details['url'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5/a').get_attribute('href')
            driver.execute_script("window.open('" + details['url'] + "', '_blank')")
            driver.switch_to.window(driver.window_handles[h])
            print("girdim")
            time.sleep(1)
            details['pdf'] = driver.find_element(By.XPATH,f'//*[@id="article-toolbar"]/a[1]').get_attribute('href')
            driver.switch_to.window(driver.window_handles[0])
            print("çıktım")
            indir_ve_kaydet(details['pdf'], "downloaded-files")
            print("indirdim")
            #details['yayın id'] = str(uuid.uuid4())
            #details['yayın adı'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5/a').text
            #details['yazar adı'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5/small[2]').text.split(", (")[0]
            #details['yayın türü'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5/small[1]/span').text
            #details['yayınlanma tarihi'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5/small[2]').text
            #match = re.search(r'\((\d{4})\)', details['yayınlanma tarihi'] )
            # Eğer eşleşme bulunursa, yayım yılını al
            #details['yayınlanma tarihi'] = match.group(1)
            #details['yayıncı adı'] =  driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/h5').text.split("), ")[1].split(",")[0]
            #details['anahtar kelimeler (arama motorundan alınan)'] = query
            #details['anahtar kelimeler (makaleye ait)'] = driver.find_element(By.XPATH,f'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{h}]/div/div/span').text
            #details['özet'] = ''
            #details['doi numarası'] = ''
            #details['alıntı sayısı'] = ''
            print("\n------------------------------------------------CIKAN SONUCLAR----------------------------------------\n")
            print("url adresi : ", details['url'], "\n")
            print("pdf adresi : ", details['pdf'], "\n")
            #print("yayın id : ", details['yayın id'], "\n")
            #print("yayın adı : ", details['yayın adı'], "\n")
            #print("yayın türü : ", details['yayın türü'], "\n")
            #print("yazar adı : ", details['yazar adı'], "\n")
            #print("yayınlanma tarihi : ", details['yayınlanma tarihi'], "\n")
            #print("yayıncı adı : ", details['yayıncı adı'], "\n")
            #print("anahtar kelimeler (arama motorundan alınan) : ", details['anahtar kelimeler (arama motorundan alınan)'], "\n")
            #print("anahtar kelimeler (makaleye ait) : ", details['anahtar kelimeler (makaleye ait)'], "\n")
            #print("özet : ", details['özet'], "\n")
            #print("referanslar : ", details['referanslar'], "\n")
            #print("alıntı numarası : ", details['alıntı sayısı'], "\n")
            #print("doi numarası : ", details['doi numarası'], "\n")
            print("\n----------------------------------------------------------------------------------------------------\n")
            #pdf_indir_ve_tasi(details['url'][h], "", "downloaded-files")
            results.append(details)
            
        except:
            pass


#return results 



args_as_string = ' '.join(sys.argv[1:])
print(get_google_search_results(args_as_string.strip("'")))
# Ornek kullanim: "dosyaadi.py 'aranacak konu'"


print("**BITTI**")