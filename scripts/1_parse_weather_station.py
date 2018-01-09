import requests
import json


def fetch_upload_crop():
    r = requests.get('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload?filterByFormula=AND(address!="",weather_station_name="")', headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV'})
    return r.json()['records']


def update_upload_crop(id, data):
    r = requests.patch('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload/' + id, json.dumps(data), headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV', 'Content-type': 'application/json'})

    print(r.status_code, r.reason)


def find_weather_station(address):
    r = requests.get('http://52.183.94.1:8001/?backend=CWB&get=stations&q={"address":"%s"}' % address)

    return r.json()


if __name__ == '__main__':
    for upload_crop in fetch_upload_crop():
        print upload_crop['fields']['address']

        stations = find_weather_station(upload_crop['fields']['address'])

        data = {'fields': {}}
        if(stations and stations[0]['distance_km'] < 10):
            print stations[0]

            data['fields']['weather_station_id'] = stations[0]['station_id']
            data['fields']['weather_station_name'] = stations[0]['station_name']
            data['fields']['weather_station_source'] = stations[0]['source']
            data['fields']['weather_station_distance'] = stations[0]['distance_km']
        else:
            data['fields']['weather_station_id'] = '-'
            data['fields']['weather_station_name'] = '-'

        update_upload_crop(upload_crop['id'], data)
