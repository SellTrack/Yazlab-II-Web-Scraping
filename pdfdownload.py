import sys

sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')


import os
import random
import requests

from shutil import move
from datetime import datetime

def pdf_indir_ve_tasi(pdf_url, hedef_dosya, hedef_klasor):
    
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

# Örnek kullanım


# PDF'yi indir ve taşı
