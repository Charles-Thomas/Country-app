import requests
from bs4 import BeautifulSoup
import pymonggo 
import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.db.countries

def scrap_and_insert():
    markup = requests.get('https://www.scrapethissite.com/pages/simple/').text 
    soup = BeautifulSoup(markup, 'html.parser')
    countries = []

    for item in soup.select('.col-md-4.country'):
        country = {}
        country['country-name'] = item.select_one('.country-name').get_text()
        country['country-info'] = item.select_one('.country-info').get_text()
        country['country-capital'] = item.select_one('.country-capital').get_text()
        country['country-area'] = item.select_one('.country-area').get_text()
        countries.append(country)

    db.insert_many(countries)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       
        scrap_and_insert()
        return redirect(url_for('index'))

    all_countries = db.find()
    return render_template('index.html', countries=all_countries)

if __name__ == '__main__':
    app.run(debug=True)
