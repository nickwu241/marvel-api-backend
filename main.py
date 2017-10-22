from flask import Flask, jsonify
import marvel

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello World!'

@app.route('/exampleEvent')
def exampleEvent():
    event = marvel.call_events()[0]
    status, description, photo_url = marvel.parse_desc_and_photo(event)
    response = {'status': status, 'description': description, 'photo_url': photo_url}
    return jsonify(response)

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)

