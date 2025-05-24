import streamlit as st
import requests

'''
# TaxiFare Model :taxi:
'''

# st.markdown('''
# ## Remember that there are several ways to output content into your web page...
# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride
# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

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
    # Inicializa o geocodificador
    geolocator = Nominatim(user_agent="streamlit-app")
    # Faz a busca
    pickup_local = geolocator.geocode(pickup)

    if pickup_local:
        st.success("Address found!")
        pickup_longitude = pickup_local.longitude
        pickup_latitude = pickup_local.latitude
        # Apresentar coordenadas no mapa
        # Cria DataFrame com os dois pontos
        lat_lon_df = pd.DataFrame({
                    'lat': [pickup_latitude],
                    'lon': [pickup_longitude],
                })
        # Exibe no mapa
        st.map(lat_lon_df, zoom=20)
    else:
        st.error("Address not found!")


# Dropoff
dropoff = st.text_input("Full address of drop-off location:")
if dropoff:
    # Faz a busca
    dropoff_local = geolocator.geocode(dropoff)

    if dropoff_local:
        st.write("Address found!")
        dropoff_longitude = dropoff_local.longitude
        dropoff_latitude = dropoff_local.latitude
    else:
        st.error("Address not found!")


#  Passenger count
passenger_count = st.selectbox(
    "How many passengers?",
    (list(range(1, 9)))
)

st.write("You selected:", passenger_count)


# # Apresentar coordenadas no mapa
# import pandas as pd
# # Cria DataFrame com os dois pontos
# lat_lon_df = pd.DataFrame({
#             'lat': [pickup_latitude, dropoff_latitude],
#             'lon': [pickup_longitude, dropoff_longitude],
#         })

# # Exibe no mapa
# st.map(lat_lon_df, zoom=13)

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction
# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...
# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''
# 2. Let's build a dictionary containing the parameters for our API...
# 3. Let's call our API using the `requests` package...
# 4. Let's retrieve the prediction from the **JSON** returned by the API...
# ## Finally, we can display the prediction to the user
# '''

# Build a dictionary containing the parameters for our API
params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count,
}

# Call our API using the `requests` package
response = requests.get(url, params=params)

# Retrieve the prediction from the **JSON** returned by the API
data = response.json()
st.write(response.url)
st.write("Estimated ride price", (round(data["fare"], 2)))
# Display the prediction to the user
# data[0]
