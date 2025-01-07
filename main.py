import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "c9fbb50dc0f641bfb5352315250701"  # Your WeatherAPI key

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"]
        }
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather = get_weather(city)
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
