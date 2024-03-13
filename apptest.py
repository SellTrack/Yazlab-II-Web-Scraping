import os
import sys

sys.path.insert(0, '/Users/selmanorhan/Documents/GitHub/Yazlab-II-Web-Scraping/site-packages')

from flask import Flask, render_template, request
from difflib import get_close_matches

app = Flask(__name__)

# Kelimelerin listesi
words = ["python", "flask", "javascript", "html", "css", "django", "sql", "java", "c++", "php"]

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
  # Aranan kelimeyi alma
  query = request.form.get("query")

  # Yanlış yazımı düzeltme
  suggestion = get_close_matches(query, words, n=1)[0]

  # Sonuçları gösterme
  return render_template("search.html", query=query, suggestion=suggestion)

if __name__ == "__main__":
  app.run(debug=True)
