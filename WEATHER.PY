import requests

def get_weather(city_name):
    api_key = "a6b2d14232c9ab5a748212588e6b1c4e"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        print("Requested URL:", response.url)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        
        response.raise_for_status()
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        city = data["name"]
        country = data["sys"]["country"]
        
        print(f"Weather in {city}, {country}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {description.capitalize()}")
        
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
    except Exception as err:
        print("Other error occurred:", err)

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
