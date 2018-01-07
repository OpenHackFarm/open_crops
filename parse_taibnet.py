#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
import requests
import json


def fetch_open_crop():
    r = requests.get('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop?filterByFormula=TaiBNET!=""', headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV'})
    return r.json()

def update_open_crop(id, data):
    r = requests.patch('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop/' + id, data, headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV', 'Content-type': 'application/json'})

    print(r.status_code, r.reason)


def fetch_taibnet(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    a = soup.find('table', attrs={'width': "90%", 'border': "0", 'cellpadding': "0", 'cellspacing': "0"}).findAll('a')

    family = a[1].text.split(u'  ')
    genus = a[2].text.split(u'  ')

    font = soup.find('table', attrs={'width': "90%", 'border': "0", 'cellpadding': "0", 'cellspacing': "0"}).findAll('font')

    species = font[0].text

    return {'family': family[0], 'family_zh': family[1], 'genus': genus[0], 'genus_zh': genus[1], 'species': species}

if __name__ == '__main__':
    for crop in fetch_open_crop()['records']:
        if 'family' not in crop['fields']:# or 'family_zh' not in crops['fields']:
            update_open_crop(crop['id'], json.dumps({'fields': fetch_taibnet(crop['fields']['TaiBNET'])}))
