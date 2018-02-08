#!/usr/bin/env python

import requests
import os


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


def get_wiki_page_images(title):
    r = requests.get('https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=images&format=json' % title)

    return [p['title'] for p in r.json()['query']['pages'][r.json()['query']['pages'].keys()[0]]['images']]


def get_wiki_image_origin_url(file_title):
    r = requests.get('https://commons.wikimedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=url&format=json&redirects' % file_title)

    url = r.json()['query']['pages'][r.json()['query']['pages'].keys()[0]]['imageinfo'][0]['url']

    return url

if __name__ == '__main__':
    title = 'Parsley'
    save_dir_path = 'Petroselinum crispum'

    for file_title in get_wiki_page_images(title):
        print 'Download %s...' % file_title
        url = get_wiki_image_origin_url(file_title)
        download_file(url, save_dir_path)
