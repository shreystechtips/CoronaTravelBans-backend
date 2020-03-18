import requests
import json
from urllib import request
from geotext import GeoText
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from bs4 import BeautifulSoup
from selenium import webdriver
import os 
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
# print(country_iso3_from_name("United States", exact = True))

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
usatoday = 'p',{'class':'gnt_ar_b_p'}
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
countries = {}
for site in sites:
    print(site)
    filename = os.path.join(str(site)+'.txt')
    update_html(filename, sites[site])
for site in parse:
    filename = os.path.join(site+'.txt')
    soup = open(filename, 'r').read()
    soup = BeautifulSoup(soup, features='html.parser')
    update_countries(countries,soup.findAll(parse[site]['type'],{'class',parse[site]['json']}))

def generate_final_json(countries):
    final_json = []
    for country in countries:
        temp = {}

        temp["ISO3"] = country
        temp["bans"] = countries[country]
        final_json.append(temp)
    return final_json

open(os.path.join('C:/Users/Shrey A/Git/CoronaTravel/frontend/src/data', 'test.json'), 'w+').write(json.dumps(generate_final_json(countries)))


    