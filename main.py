from flask import Flask, jsonify

import random
import marvel

spider_man_events = None

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello World!'

@app.route('/exampleEvent')
def exampleEvent():
    event = marvel.events()['results'][0]
    response = marvel.wrap_parsed(marvel.parse_desc_and_photo(event))
    return jsonify(response)

@app.route('/event/random')
def randomEvent():
    if not spider_man_events:
        feteh_globals()
    response = marvel.wrap_parsed(marvel.parse_desc_and_photo(random.choice(spider_man_events)))
    return jsonify(response)

@app.route('/event/<int:event_id>')
def showEvent(event_id):
    if not spider_man_events:
        feteh_globals()
    response = marvel.wrap_parsed(marvel.parse_desc_and_photo(spider_man_events[0]))
    return jsonify(response)

@app.route('/event/<int:event_id>/html')
def showEventHtml(event_id):
    if not spider_man_events:
        feteh_globals()
    status, description, photo_url = marvel.parse_desc_and_photo(spider_man_events[event_id])
    return '<h1>{:s}</h1><img src={:s}>'.format(description, photo_url)

def fetch_globals():
    global spider_man_events
    params = marvel.get_auth_params()
    params['characters'] = marvel.CHAR_ID_MAP['Spider-Man']
    params['offset'] = 0
    params['limit'] = 100
    spider_man_events = marvel.events(params)['results']
    # print(spider_man_events)

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    fetch_globals()
    app.run(host='0.0.0.0', port=8080, debug=True)

