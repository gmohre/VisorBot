import json
import urllib2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C:\ow.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

OW_API_HEADERS = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
QUOTES = {}

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(pow(2, 7)), nullable=False)
    quotes = orm.relationship("Quote", backref="hero")

    def __repr__(self):
        return '<Hero %r>' % self.name

class Quote(db.Model):
    __tablename__ = 'quote'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(pow(2, 10)))
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))

    def __repr__(self):
        return '<Quote %r - %r>' % (self.hero, self.text)

def hero():
    h=Hero(name='Ana')
    q=Quote(text='Hi', hero=h)
    db.session.add(h)
    db.session.add(q)
    db.session.commit()



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
