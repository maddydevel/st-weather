import requests
import streamlit as st
import pandas as pd

# Define the URL for the weather API
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Define the default location and API key
DEFAULT_LOCATION = "London, UK"
API_KEY = "7edb546a1f1de6d1c5ae3cd3f9850076"

# Define the weather data columns we want to display
WEATHER_COLUMNS = ["Temperature", "Feels like", "Humidity", "Pressure"]

# Define the available output formats
OUTPUT_FORMATS = {
    "Table": "table",
    "Line Chart": "line_chart",
    "Bar Chart": "bar_chart",
    "Area Chart": "area_chart",
}

# Define a function to fetch the weather data for a given location
def fetch_weather_data(location):
    params = {"q": location, "appid": API_KEY, "units": "metric"}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
        }
    else:
        st.warning("Unable to fetch weather data.")
        return None

# Define the Streamlit app
def app():
    # Set the page title
    st.set_page_config(page_title="Weather App", page_icon=":partly_sunny:")

    # Define the sidebar inputs
    location = st.sidebar.text_input("Location", DEFAULT_LOCATION)
    output_format = st.sidebar.selectbox("Output Format", list(OUTPUT_FORMATS.keys()))

    # Fetch the weather data
    weather_data = fetch_weather_data(location)

    # Display the weather data
    if weather_data is not None:
        st.header(f"Weather in {weather_data['location']}")
        if output_format == "table":
            df = pd.DataFrame([weather_data], columns=WEATHER_COLUMNS)
            st.table(df)
        else:
            chart_data = pd.Series(weather_data).drop("location")
            st.write(f"### {output_format}")
            st.set_option("deprecation.showPyplotGlobalUse", False)
            st.pyplot(getattr(chart_data, OUTPUT_FORMATS[output_format])())
    
# Run the app
if __name__ == "__main__":
    app()
