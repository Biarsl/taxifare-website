import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="NYC Taxi Fare Predictor", page_icon="🚖")

st.title("NYC Taxi Fare Predictor 🚕")

# We ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# We answer with the prediction (taxi fare value).

# Datetime
from datetime import datetime

date = st.date_input("Ride date", value="today")
time = st.time_input("Ride time", value=datetime.now())
pickup_datetime = datetime.combine(date, time)

st.write("Selected date and time:", pickup_datetime)


pickup_longitude = None
pickup_latitude = None
dropoff_longitude = None
dropoff_latitude = None

# Pickup
from geopy.geocoders import Nominatim
import pandas as pd

pickup = st.text_input("Full address of pick-up location:")
if pickup:
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="streamlit-app")
    # Search
    pickup_local = geolocator.geocode(pickup)

    if pickup_local:
        st.success("Address found!")
        pickup_longitude = pickup_local.longitude
        pickup_latitude = pickup_local.latitude
        # Display coordinates on the map
        # Create a DataFrame with the two points
        lat_lon_df = pd.DataFrame({
                    'lat': [pickup_latitude],
                    'lon': [pickup_longitude],
                })
        # Display on map
        st.map(lat_lon_df, zoom=15)
    else:
        st.error("Address not found!")


# Dropoff
dropoff = st.text_input("Full address of drop-off location:")
if dropoff:
    # Search
    dropoff_local = geolocator.geocode(dropoff)

    if dropoff_local:
        st.write("Address found!")
        dropoff_longitude = dropoff_local.longitude
        dropoff_latitude = dropoff_local.latitude
        # Display coordinates on the map
        # Create a DataFrame with the two points
        lat_lon_df_2 = pd.DataFrame({
                    'lat': [dropoff_latitude],
                    'lon': [dropoff_longitude],
                })
        # Display on map
        st.map(lat_lon_df_2, zoom=15)
    else:
        st.error("Address not found!")


#  Passenger count
passenger_count = st.selectbox(
    "How many passengers?",
    (list(range(1, 9)))
)

st.write("You selected:", passenger_count)

#Prediction
if st.button("Estimate Fare"):
    if None in [pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude]:
        st.warning("Please enter valid addresses for both locations!")
    else:
        params = {
            'pickup_datetime': pickup_datetime,
            'pickup_longitude': pickup_longitude,
            'pickup_latitude': pickup_latitude,
            'dropoff_longitude': dropoff_longitude,
            'dropoff_latitude': dropoff_latitude,
            'passenger_count': passenger_count,
        }
        
        try:
            response = requests.get('https://taxifare.lewagon.ai/predict', params=params)
            response.raise_for_status()
            data = response.json()
            fare = round(data["fare"], 2)
            st.success(f"Estimated ride price: ${fare}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting prediction: {str(e)}")
