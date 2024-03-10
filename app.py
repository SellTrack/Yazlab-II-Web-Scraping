import os
import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    
    pdf_klasoru = 'downloaded-files'  # Klasör yolunu düzenleyin
    pdf_dosyalar = [dosya for dosya in os.listdir(pdf_klasoru) if dosya.endswith('.pdf')]

    return render_template('index.html', pdf_dosyalar=pdf_dosyalar)

if __name__ == '__main__':
    app.run(debug=True)
