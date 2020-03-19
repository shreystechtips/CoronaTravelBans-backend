import requests
import json
from urllib import request
from geotext import GeoText
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from bs4 import BeautifulSoup
from selenium import webdriver
import os 
import time
import pyrebase
import base64
from dotenv import load_dotenv
#Firebase setup
load_dotenv()
def generate_google_service(fileName):
    open(fileName, "w+").write(base64ToString(os.getenv("FIREBASE_SERVICE_CODE")))
    return fileName


def base64ToString(b):
    return base64.b64decode(bytes(b, "utf-8").decode('unicode_escape')).decode('utf-8')


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))
config = {
    "apiKey": os.getenv("FIREBASE_KEY"),
    "authDomain": str(os.getenv("FIREBASE_PROJ_NAME")) + ".firebaseapp.com",
    "storageBucket": str(os.getenv("FIREBASE_PROJ_NAME")) + ".appspot.com",
    "databaseURL": "https://" + str(os.getenv("FIREBASE_PROJ_NAME")) + ".firebaseio.com",
    "serviceAccount": generate_google_service("service.json")
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

try:
    # INIT FIREBASE
    os.remove("service.json")
except:
    None

iso = json.loads(open('./data/iso3.json','r').read())
names = json.loads(open('./data/names.json','r').read())
def country_iso3_from_name(name, exact = False):
    results = [x for x in names if ( name.lower().strip() == names[x].lower().strip() if exact else name.lower().strip() in names[x].lower().strip())]
    iso3 = []
    for result in results:
        iso3.append(iso[result])
    return iso3

def iso2_to_iso3(iso2):
    if iso2 in iso:
        return iso[iso2]
    else:
        return ''

def update_countries(countries, iterator):
    lastCountry = ""
    for para in iterator:
        places = GeoText(para.text)
        loc = list(places.country_mentions)
        if 'strong' in str(para):
            if len(loc) > 0 and loc[0] != '':
                countries[iso2_to_iso3(loc[0])] = []
                lastCountry = iso2_to_iso3(loc[0])
        else:
            for itm in loc:
                itm_new = iso2_to_iso3(itm)
                if itm_new != lastCountry:
                    countries[lastCountry].append(itm_new)
            if(lastCountry != ""):
                countries[lastCountry] = list(set(countries[lastCountry]))
    print(countries)

sites = {'usatoday':"https://www.usatoday.com/story/travel/news/2020/03/17/coronavirus-travel-bans-countries-impose-travel-restrictions/5058513002/",
        'cnn': 'https://www.cnn.com/travel/article/coronavirus-travel-bans/index.html'}
parse = {'usatoday':{'type':'p','json':'gnt_ar_b_p'}
    ,
    'cnn':
            {'type':'div',
            'json':'Paragraph__component'}
    }


def update_html(file,url):
    driver = webdriver.PhantomJS() 
    driver.get(url)
    soup = driver.execute_script("return document.body.outerHTML;")
    open(file,'w+').write(str(soup))

def generate_final_json(countries):
    final_json = []
    for country in countries:
        temp = {}
        temp["ISO3"] = country
        temp["bans"] = countries[country]
        final_json.append(temp)
    return final_json
while True:
    countries = {}
    for site in sites:
        print('downloading ', site)
        filename = os.path.join(str(site)+'.txt')
        update_html(filename, sites[site])
    for site in parse:
        print('parsing ', site)
        filename = os.path.join(site+'.txt')
        soup = open(filename, 'r').read()
        soup = BeautifulSoup(soup, features='html.parser')
        update_countries(countries,soup.findAll(parse[site]['type'],{'class',parse[site]['json']}))
    FILE_NAME = 'data.json'
    FILE_PATH = os.path.join('data', FILE_NAME)
    print('writing')
    open(FILE_PATH, 'w+').write(json.dumps(generate_final_json(countries)))
    storage.child('/')
    storage.child('parsed_data.json').put(FILE_PATH)
    print('written')
    time.sleep(600000)


    