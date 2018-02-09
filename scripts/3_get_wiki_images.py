#!/usr/bin/env python
#coding: utf-8

import requests
import os
from file_utils import search_file
import urllib


RESCAN = False


def fetch_open_crop():
    r = requests.get('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop?filterByFormula=variety_zh="(總稱)"', headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV'})

    return r.json()


# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url, save_dir_path='', filename=None):
    if save_dir_path and not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)

    if filename:
        local_filename = filename
    else:
        local_filename = url.split('/')[-1]

    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(os.path.join(save_dir_path, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian

    return local_filename


def get_wiki_page_images(url):
    title = url.split('/')[-1]

    r = requests.get('https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=images&format=json' % title)

    return [p['title'] for p in r.json()['query']['pages'][r.json()['query']['pages'].keys()[0]]['images']]


def get_wiki_image_origin_url(file_title):
    r = requests.get('https://commons.wikimedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=url&format=json&redirects' % file_title)

    if 'imageinfo' in r.json()['query']['pages'][r.json()['query']['pages'].keys()[0]]:
        url = r.json()['query']['pages'][r.json()['query']['pages'].keys()[0]]['imageinfo'][0]['url']

        return url
    else:
        return ''

if __name__ == '__main__':
    crops = fetch_open_crop()['records']

    for crop in crops:
        if 'wiki' in crop['fields'] and 'species' in crop['fields']:
            title = crop['fields']['wiki'].split('/')[-1]
            species = crop['fields']['species']
            species = crop['fields']['species_zh']
            save_dir_path = os.path.join('Images', crop['fields']['species_zh'] + ' - ' + crop['fields']['species'])

            if title and save_dir_path:
                if RESCAN or not os.path.exists(save_dir_path):
                    print '* %s -> %s' % (title, species)
                    for file_title in get_wiki_page_images(title):
                        # url = get_wiki_image_origin_url(urllib.quote_plus(file_title))
                        url = get_wiki_image_origin_url(file_title.replace('&', '%26'))
                        if url is '' or search_file(url.split('/')[-1], save_dir_path):
                            print 'Pass %s...' % file_title
                        else:
                            print 'Download %s...' % file_title
                            download_file(url, save_dir_path)
