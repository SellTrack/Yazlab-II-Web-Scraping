import sys
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages/beautifulsoup4-4.12.3')  # 'site-packages/selenium' kısmını kendi yüklü olduğunuz yerle değiştirin
import os
import shutil

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pdfminer.high_level import extract_text

# Elasticsearch bağlantısı
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# PDF dosyasından içeriği çıkarma
def extract_pdf_content(pdf_path):
    with open(pdf_path, 'rb') as f:
        text = extract_text(f)
    return text

# Elasticsearch'a PDF içeriğini eklemek için belgeleri oluşturma
def generate_documents(pdf_files):
    for pdf_file in pdf_files:
        content = extract_pdf_content(pdf_file)
        yield {
            '_index': 'pdf_index',
            '_source': {
                'filename': pdf_file,
                'content': content
            }
        }

# PDF dosyalarının bulunduğu dizin
pdf_directory = '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/static/downloaded-files/deep learning'

# Tüm PDF dosyalarını indeksleme
pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']  # PDF dosyalarının listesi
bulk(es, generate_documents(pdf_files))

# Belirli bir terimle arama yapma
search_term = 'your_search_term'
search_body = {
    'query': {
        'match': {
            'content': search_term
        }
    }
}
results = es.search(index='pdf_index', body=search_body)
print(results)
