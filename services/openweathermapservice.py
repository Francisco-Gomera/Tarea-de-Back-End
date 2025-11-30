import requests

def get_meteorological_data(city: str, api_key: str):
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    print(response)
    if response.status_code != 200:
        return {"error": "Ciudad no encontrada"}    
    weather_data = response.json()
    return weather_data