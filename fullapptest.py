import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages/beautifulsoup4-4.12.3')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
import os
import shutil

from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_pymongo import PyMongo
from datetime import datetime
from dergipark_search import get_dergipark_search_results  # dergipark_search.py dosyanızdan get_dergipark_search_results fonksiyonunu import edin
from spellchecker import SpellChecker

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27018/Yazlab'  # MongoDB URI'nizi buraya ekleyin
mongo = PyMongo(app)

DOSYA_DIZINI = '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/static/downloaded-files'

spell_checker = SpellChecker()

def find_spelling_errors(text):
    words = text.split()
    corrected_words = [spell_checker.correction(word) for word in words]
    if corrected_words == "":
        corrected_words = text
    return " ".join(corrected_words)

class Yayin:
    def __init__(self, data):
        self.yayin_id = data.get("yayin_id")
        self.yayin_adi = data.get("yayin_adi")
        self.yazarlar = data.get("yazarlar", [])
        self.yayin_turu = data.get("yayin_turu")
        self.yayinlanma_tarihi = data.get("yayinlanma_tarihi")
        self.yayinevi_adi = data.get("yayinevi_adi")
        self.anahtar_kelimeler_makale = data.get("anahtar_kelimeler_makale", [])
        self.ozet = data.get("ozet")
        self.referanslar = data.get("referanslar", [])
        self.alinti_sayisi = data.get("alinti_sayisi", 0)
        self.doi_numarasi = data.get("doi_numarasi")
        self.url_adresi = data.get("url_adresi")
        self.pdf_adresi = data.get("pdf_adresi")
        self.dosya_yolu = data.get("dosya_yolu")
        self.aratilan_kelime_id = data.get("aratilan_kelime_id")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        aranan_kelime = request.form['aranan_kelime']
        if aranan_kelime != "":  
            # Yazım hatalarını düzelt
            corrected_keyword = find_spelling_errors(aranan_kelime)
            # Arama sonuçlarını getir
            print("Aranan kelime : ", corrected_keyword)
            sonuclar = get_dergipark_search_results(corrected_keyword)
            print("\n", sonuclar)
            for sonuc in sonuclar:
                yayin_data = {
                    "yayin_id": sonuc['yayın id'],
                    "yayin_adi": sonuc['yayın adı'],
                    "yazarlar": sonuc['yazar adı'].split(", "),
                    "yayin_turu": sonuc['yayın türü'],
                    "yayinlanma_tarihi": sonuc['yayınlanma tarihi'],
                    "yayinevi_adi": sonuc['yayıncı adı'],
                    "anahtar_kelimeler_makale": sonuc['anahtar kelimeler (makaleye ait)'].split(", "),
                    "ozet": sonuc['özet'],
                    "referanslar": sonuc['referanslar'],
                    "alinti_sayisi": sonuc['alıntı sayısı'],
                    "doi_numarasi": sonuc['doi numarası'],
                    "url_adresi": sonuc['url'],
                    "pdf_adresi": sonuc['pdf'],
                    "dosya_yolu": sonuc['dosya_yolu']
                }
                # Yayın verilerini MongoDB'ye kaydet
                mongo.db.sonuclar.insert_one(yayin_data)
        return redirect(url_for('index'))  
    else:
        yayinlar_from_mongo = mongo.db.sonuclar.find()
        yayinlar = [Yayin(data=yayin) for yayin in yayinlar_from_mongo]
        return render_template('index.html', yayinlar=yayinlar)

@app.route('/dosya_tarayici')
def dosya_tarayici():
    dosyalar = os.listdir(DOSYA_DIZINI)
    return render_template('dosya_tarayici.html', dosyalar=dosyalar, dosya_dizini=DOSYA_DIZINI)

@app.route('/dosya_goster/<dosya_adi>')
def dosya_goster(dosya_adi):
    dosya_yolu = os.path.join(DOSYA_DIZINI, dosya_adi)
    if os.path.exists(dosya_yolu):
        if dosya_adi.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf')):
            return send_file(dosya_yolu)
        elif os.path.isdir(dosya_yolu):
            dosyalar = os.listdir(dosya_yolu)
            return render_template('dosya_tarayici.html', dosyalar=dosyalar, dosya_dizini=dosya_yolu)
        elif os.path.isfile(dosya_yolu):
            return send_file(dosya_yolu)
    return f"{dosya_adi} adlı dosya bulunamadı."

if __name__ == '__main__':
    app.run(debug=True)
