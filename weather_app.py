import streamlit as st
import requests
import json

# API endpoint for weather data
api_url = 'https://api.openweathermap.org/data/2.5/weather'

# Set up API parameters
params = {
    'appid': '7edb546a1f1de6d1c5ae3cd3f9850076',
    'units': 'metric',
    'cnt': 1,
    'q': 'London',
}

# Get weather data for London
response = requests.get(api_url, params=params)

if response.status_code == 200:
    # Parse JSON response
    data = json.loads(response.text)
    city = data['weather'][0]['name']
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    icon = data['weather'][0]['icon']

    # Display weather data in Streamlit app
    st.title('Weather in London')
    st.write('Temperature: ', temperature, '°C')
    st.write('Description: ', description)
    st.write('Icon: ', icon)
    st.write('City: ', city)
else:
    # Handle error response
    st.write('Error:', response.status_code)
