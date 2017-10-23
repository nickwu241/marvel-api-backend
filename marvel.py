import hashlib
import json
import os
import time
import requests

PUB_KEY = os.environ.get('MARVEL_PUB_KEY')
PRIV_KEY = os.environ.get('MARVEL_PRIV_KEY')

if not PUB_KEY or not PRIV_KEY:
    with open('secrets.json') as f:
        secrets = json.load(f)
    PUB_KEY = secrets['MARVEL_PUB_KEY']
    PRIV_KEY = secrets['MARVEL_PRIV_KEY']
    if not PUB_KEY or not PRIV_KEY:
        raise Exception("Make sure MARVEL_PUB_KEY and MARVEL_PRIV_KEY is present.")

CHAR_ID_MAP = {'Spider-Man': 1009610}

BASE_API = "http://gateway.marvel.com"
EVENTS = "/v1/public/events"
STORIES = "/v1/public/stories"

def get_ts_and_hash():
    ts = str(int(time.time()))
    hash = hashlib.md5((str(ts) + PRIV_KEY + PUB_KEY).encode()).hexdigest()
    return (ts, hash)

def get_auth_params():
    ts, hash = get_ts_and_hash()
    return {'ts': ts, 'apikey': PUB_KEY, 'hash': hash}

def events(params={}):
    params = {**params, **get_auth_params()}
    response = requests.get(BASE_API + EVENTS, params=params).json()
    assert response['code'] == 200
    return response['data']

def parse_desc_and_photo(event):
    desc = event['description']
    if 'thumbnail' in event:
        image_url = event['thumbnail']['path'] + '.' + event['thumbnail']['extension']
    else:
        image_url = None
    status = 200
    return (status, desc, image_url)

def wrap_parsed(parsed_tuple):
    status, description, photo_url = parsed_tuple
    return {'status': status, 'description': description, 'photo_url': photo_url}

def main():
    event = call_events()['results'][0]
    print(parse_desc_and_photo(event))

if __name__ == '__main__':
    #main()
    import pprint
    response = events({'characters': CHAR_ID_MAP['Spider-Man']}) 
    offset = 0
    total = response['total']
    while offset < total:
        print(offset)
        params = get_auth_params()
        params['characters'] = CHAR_ID_MAP['Spider-Man']
        params['offset'] = offset
        params['limit'] = 100
        response = events(params) 
        for res in response['results']:
            print(parse_desc_and_photo(res))
        offset += 100
        break
    # pprint.pprint(response)

