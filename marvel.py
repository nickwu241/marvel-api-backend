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

BASE_API = "http://gateway.marvel.com"
EVENTS = "/v1/public/events"

def get_ts_and_hash():
    ts = str(int(time.time()))
    hash = hashlib.md5((str(ts) + PRIV_KEY + PUB_KEY).encode()).hexdigest()
    return (ts, hash)

def get_auth_params():
    ts, hash = get_ts_and_hash()
    return {'ts': ts, 'apikey': PUB_KEY, 'hash': hash}

def call_events():
    response = requests.get(BASE_API + EVENTS, params=get_auth_params()).json()
    assert response['code'] == 200
    return response['data']['results']

def parse_desc_and_photo(event):
    desc = event['description']
    image_url = event['thumbnail']['path'] + '.' + event['thumbnail']['extension']
    status = 200
    return (200, desc, image_url)

def main():
    event = call_events()[0]
    print(parse_desc_and_photo(event))

if __name__ == '__main__':
    main()
