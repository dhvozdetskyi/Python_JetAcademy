from flask import Flask, request, render_template, redirect, flash
import sys
from datetime import datetime, timezone
import requests
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    """Data model for cities."""

    __tablename__ = 'City'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(20),
        index=True,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '<City %r>' % self.name


db.create_all()

# with open('../../key.txt', 'r') as f:
#    api_key = f.readline()

api_key = '482a4ee737249235ca8e7ef4ccdb5493'


weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"
dict_with_weather_info = dict()


def get_daytime(time, response):
    """
    :param time: timestamp in unix seconds
    :param response: response from weather api
    :return: str day/evening-morning/night
    """
    hr_gap = 1
    if response['sys']['sunrise'] < time <= response['sys']['sunset'] - 3600 * hr_gap:
        return "day"
    # if hr_gap before and after sunrise or hr_gap before after sunset
    elif response['sys']['sunrise'] - 3600 * hr_gap < time < response['sys']['sunrise'] + 3600 * hr_gap or \
            response['sys']['sunset'] - 3600 * hr_gap < time < response['sys']['sunset'] + 3600 * hr_gap:
        return "evening-morning"
    else:
        return "night"


def call_weather_api(city, id, url, key, units="metric"):
    """
    :param city: city name
    :param url: url of weather api site
    :param key: API key
    :param units: metric/imperial
    :return: dict{city:response}
             with response
             condition: weather state
             temp: temperature
             time_now: current time UTC
             time_of_day: day state
    """
    params = {'q': city, 'appid': key, 'units': units}
    r = requests.get(url, params=params)
    if r.status_code != requests.codes.ok:
        flash("The city doesn't exist!")
        return dict()
    else:
        resp = r.json()
        time_now = int(datetime.now(tz=timezone.utc).timestamp())
        time_of_day = get_daytime(time_now, resp)
        return {resp['name']: {'id': id,
                               'condition': resp['weather'][0]['main'],
                               'temp': str(resp['main']['temp']),
                               'time_now': time_now, 'time_of_day': time_of_day}}


@app.route('/')
def index():
    query = City.query
    dict_with_weather_info = dict()
    for city in query:
        dict_with_weather_info.update(call_weather_api(city.name, city.id, weather_endpoint, api_key))

    return render_template('index.html', weather=dict_with_weather_info)

@app.route('/', methods=['POST'])
def add_city():
    city = request.form['city_name']
    if City.query.filter_by(name=city).first():
        flash("The city has already been added to the list!")
    elif call_weather_api(city, 0, weather_endpoint, api_key) != dict():
        db.session.add(City(name=city))
        db.session.commit()

    return redirect('/')


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
