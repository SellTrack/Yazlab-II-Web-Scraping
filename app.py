import os
import sys

sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')
from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27018/Documents'
mongo = PyMongo(app)

class Yayin:
    def __init__(self, data):
        self.yayinId = data.get("yayinId")
        self.yayin_adi = data.get("yayin_adi")
        self.yazarlar = data.get("yazarlar", [])
        self.yayin_turu = data.get("yayin_turu")
        self.yayinlanma_tarihi = datetime.strptime(data.get("yayinlanma_tarihi"), "%m-%d-%Y") if data.get("yayinlanma_tarihi") else None
        self.yayinci_adi = data.get("yayinci_adi")
        self.anahtar_kelimeler_arama = data.get("anahtar_kelimeler_arama", [])
        self.anahtar_kelimeler_makale = data.get("anahtar_kelimeler_makale", [])
        self.ozet = data.get("ozet")
        self.referanslar = data.get("referanslar", [])
        self.alinti_sayisi = data.get("alinti_sayisi", 0)
        self.doi_numarasi = data.get("doi_numarasi")
        self.url_adresi = data.get("url_adresi")

@app.route('/')
def index():
    # MongoDB'den yayinları al
    yayinlar_from_mongo = mongo.db.Docs.find()

    # Alınan yayınları Yayin sınıfına dönüştür
    yayinlar = [Yayin(data=yayin) for yayin in yayinlar_from_mongo]

    # HTML şablonunu render et ve yayınları gönder
    return render_template('index3.html', yayinlar=yayinlar)

if __name__ == '__main__':
    app.run(debug=True)