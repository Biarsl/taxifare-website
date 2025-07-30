import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="NYC Taxi Fare Predictor", page_icon="🚖", layout="wide")

# Função para adicionar imagem de fundo
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
             background-opacity: 0.1;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# CSS para o título
st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    font-weight: bold;
    color: #FFFFFF;
    text-shadow: 2px 2px 4px #000000;
}
</style>
""", unsafe_allow_html=True)

# Título centralizado com emoji e estilo
st.markdown('<p class="big-font">NYC Taxi Fare Predictor 🚕</p>', unsafe_allow_html=True)

'''
NY Taxi Fare prediction :taxi:
'''

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
            
# # Retrieve the prediction from the **JSON** returned by the API
# data = response.json()
# st.write(response.url)

# # Display the prediction to the user
# st.write("Estimated ride price", (round(data["fare"], 2)))
