import json
import urllib2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}
OW_API_HEADERS = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
QUOTES = {}

@app.route('/populate_data')
def populate_data():
    global QUOTES
    def _load_heroes():
        req = urllib2.Request(url='https://overwatch-api.net/api/v1/hero', headers=OW_API_HEADERS)
        page = urllib2.urlopen(req)
        data = json.loads(page.read())['data']
        return data

    def _load_quotes(hero):
        url = 'https://overwatch-api.net/api/v1/hero/' + str(hero['id'])
        req = urllib2.Request(url=url, headers=OW_API_HEADERS)
        page = urllib2.urlopen(req)
        data = json.loads(page.read())
        quotes = [quote['name'] for quote in data['rewards'] if quote['type']['name'] == 'voice line']
        return quotes

    try:
        QUOTES = json.load(open('data.txt'))
    except:
        print('loading data')
    if not len(QUOTES.items()):
        heroes = _load_heroes()
        print('getting quotes')
        for hero in heroes:
            QUOTES["hero"+str(hero['id'])]= _load_quotes(hero)
        with open("data.txt", 'w') as outfile:
            json.dump(QUOTES, outfile)
    return render_template('hero.html', **QUOTES)

@socketio.on('value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)

@socketio.on('client connect')
def connected(message):
    print(message)

@app.route('/')
def index():
    return render_template('index.html', **values)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
