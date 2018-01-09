import requests
import json
import dateutil.parser


def fetch_upload_crop():
    r = requests.get('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload?filterByFormula=AND(weather_station_id!="",temperature="",exif_datetime>"2000-01-01")', headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV'})
    return r.json()['records']


def update_upload_crop(id, data):
    r = requests.patch('https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload/' + id, json.dumps(data), headers={'Authorization': 'Bearer key5cOGuWwOqmI1DV', 'Content-type': 'application/json'})

    print(r.status_code, r.reason)


def get_month_temperature(id, name, month):
    r = requests.get('https://raw.githubusercontent.com/OpenHackFarm/CODiS_carwler/master/data/%s_%s/%s.json' % (id, name, month))

    return r.json()


if __name__ == '__main__':
    for upload_crop in fetch_upload_crop():
        print upload_crop['fields']['exif_datetime']

        dt = dateutil.parser.parse(upload_crop['fields']['exif_datetime'])
        month = dt.strftime('%Y-%m')

        try:
            json_data = get_month_temperature(upload_crop['fields']['weather_station_id'], upload_crop['fields']['weather_station_name'], month)
        except:
            print 'JSON file not on GitHub.'
            continue

        payload_data = {'fields': {}}
        if json_data:
            payload_data['fields']['temperature'] = float(json_data[str(dt.day)]['Temperature'])
        else:
            payload_data['fields']['temperature'] = -99

        print payload_data['fields']['temperature']

        update_upload_crop(upload_crop['id'], payload_data)
