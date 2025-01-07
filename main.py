from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "c9fbb50dc0f641bfb5352315250701"  # Your WeatherAPI key

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=yes&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "current": {
                "city": data["location"]["name"],
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],  # Extracting text here
                "humidity": data["current"]["humidity"],
                "wind_speed": data["current"]["wind_kph"],
                "air_quality": data["current"]["air_quality"],  # Includes AQI
            },
            "forecast": [
                {
                    "date": day["date"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                    "condition": day["day"]["condition"]["text"],  # Extracting text here
                    "emoji": get_weather_emoji(day["day"]["condition"]["text"]),  # Add emoji
                    "hourly": [
                        {
                            "time": hour["time"],
                            "temp": hour["temp_c"],
                            "condition": hour["condition"]["text"],
                            "icon": hour["condition"]["icon"],
                        }
                        for hour in day["hour"]
                    ],  # Hourly weather for the day
                }
                for day in data["forecast"]["forecastday"]
            ],
            "emoji": get_weather_emoji(data["current"]["condition"]["text"])  # Add emoji for current weather
        }
    return None

# Function to get weather emoji based on condition
def get_weather_emoji(condition):
    condition = condition.lower()
    if 'sunny' in condition:
        return '☀️'
    elif 'cloudy' in condition:
        return '☁️'
    elif 'rain' in condition:
        return '🌧️'
    elif 'snow' in condition:
        return '❄️'
    elif 'fog' in condition:
        return '🌫️'
    elif 'thunderstorm' in condition:
        return '⛈️'
    elif 'partly cloudy' in condition:
        return '⛅'
    return '🌤️'  # Default emoji

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather = get_weather(city)
    return render_template('index.html', weather=weather)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
