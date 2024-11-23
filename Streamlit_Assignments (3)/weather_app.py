import streamlit as st
import requests
import pandas as pd

st.title("WEATHER DATA VIEWER")

API_URL = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "661e31209c95328976a7cdc51aebf03f"

city_name = st.text_input("Enter a city name")

if st.button("Fetch Weather"):
    if city_name:
        # API call to get city coordinates (since the forecast API requires lat/lon)
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_KEY}"
        geo_response = requests.get(geo_url).json()

        if geo_response:
            #extracting lat/lon
            lat, lon = geo_response[0]['lat'], geo_response[0]['lon']

            #fetching data using lat/lon
            weather_params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
            weather_response = requests.get(API_URL, params=weather_params).json()

            if weather_response.get("cod") == "200":
                st.subheader(f"Weather Forecast for {city_name.capitalize()}")

                #showing data in table
                forecast_data = []
                for forecast in weather_response['list'][:5]:  # Show the first 5 forecasts
                    dt_txt = forecast["dt_txt"]
                    temp = forecast["main"]["temp"]
                    humidity = forecast["main"]["humidity"]
                    wind_speed = forecast["wind"]["speed"]
                    precipitation = forecast["rain"]["3h"] if "rain" in forecast else 0.0
                    weather_desc = forecast["weather"][0]["description"]
                    
                    forecast_data.append([dt_txt, temp, humidity, wind_speed, precipitation, weather_desc.capitalize()])

                forecast_df = pd.DataFrame(forecast_data, columns=[
                    "Date & Time", "Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Precipitation (mm)", "Weather Description"
                ])

                st.table(forecast_df)
            else:
                st.error("Error fetching weather forecast. Please try again.")
        else:
            st.error(f"City '{city_name}' not found. Please check the name.")
    else:
        st.warning("Please enter a city name.")
