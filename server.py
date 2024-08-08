from flask import Flask, request, render_template
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not bool(city.strip()):
        city = 'Ankara'

    data = get_current_weather(city)

    if not data['cod'] == 200:
        return render_template('error.html', city=city)

    temp_celsius = (data['main']['temp'] - 32) * 5 / 9
    feels_like_celsius = (data['main']['feels_like'] - 32) * 5 / 9

    return render_template(
        'weather.html',
        title=data['name'],
        status=data['weather'][0]['description'],
        temp=f'{temp_celsius:.1f}',
        feels_like=f'{feels_like_celsius:.1f}'
    )


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=3000)

