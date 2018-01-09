import fnmatch
import os
import exifread
import requests
import json
import datetime

IMAGE_PATH = '/home/farmer/DOCKER_DATA/pictshareuploads/'


def fetch_open_crop():
    r = requests.get('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload?filterByFormula=exif_datetime=""', headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV'})
    return r.json()['records']


def update_open_crop(id, data):
    r = requests.patch('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload/' + id, data, headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV', 'Content-type': 'application/json'})

    print(r.status_code, r.reason)


# https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
def search_file(search_file, search_path):
    for root, dirnames, filenames in os.walk(search_path):
        for filename in fnmatch.filter(filenames, search_file):
            return os.path.join(root, filename)


def read_exif_data(path_name,):
    f = open(path_name, 'rb')

    return exifread.process_file(f)


if __name__ == '__main__':
    for i in fetch_open_crop():
        img_f = i['fields']['image_url'].split('/')[-1]
        find_file = search_file(img_f, IMAGE_PATH)
        if find_file:
            print find_file

            tags = read_exif_data(find_file)
            if 'Image DateTime' in tags:
                print tags['Image DateTime']

                old_datetime = str(tags['Image DateTime'])
                new_datetime = datetime.datetime.strptime(old_datetime, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')

                update_open_crop(i['id'], json.dumps({'fields': {'exif_datetime': new_datetime}}))
            else:
                update_open_crop(i['id'], json.dumps({'fields': {'exif_datetime': '1970-01-01'}}))
