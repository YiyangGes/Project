import math
from datetime import datetime
import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image


# Create the header section
image = Image.open('download.png')
col0, col1, col2 = st.columns([0.3, 0.65, 3])  # Adjust the ratio based on your aesthetic preference

col1.image(image, width = 80)
col2.title('NYC Airbnb Navigator')
st.write("Welcome to NYC Airbnb Navigator! Find the perfect Airbnb rental in New York City with ease. Select your preferred borough and neighborhood, set your price range, and explore available listings. Get started now to discover your ideal NYC stay!")
# @st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.dataframe(df.head(10))

# All feature sections ------------------------------------------------

st.subheader('Pick Your Preferred Location :anchor: And Price Range :moneybag:', divider = 'rainbow')

# Drop down box for the five districts, and get the option
option = st.selectbox(
    'Which boroughs do you live in',
    df['neighbourhood_group'].unique())
all_in_district = df[df['neighbourhood_group'] == option]

# Multi-select box for neighbourhood
multi_options = all_in_district['neighbourhood'].unique()
st_ms = st.multiselect("Select Neighbourhood Groups in NYC", multi_options, multi_options[:2])
filtered_with_nh = all_in_district[df["neighbourhood"].isin(st_ms)]

# Price slider
values = st.slider("Select a price range :money_mouth_face:", float(df.price.min()), 1000., (50., 150.))

# Draw table finally!
final_df_pr = filtered_with_nh[(filtered_with_nh['price'] >= values[0]) & (filtered_with_nh['price'] <= values[1])]
st.dataframe(final_df_pr)

# set neighbourhood str
if len(st_ms) > 1: # if there is more than one neighbourhood selected, convert the list to a correct sentences
    neighbourhood_str = ", ".join(st_ms[0:-1]) + ', and '+st_ms[-1]
else:
    neighbourhood_str = st_ms[0]

# print the final str
result_str = f"Total {len(final_df_pr)} housing rental are found in {neighbourhood_str} within {option} with price between {values[0]} and {values[1]}"
st.write(result_str)

if len(final_df_pr) != 0:
    # initialize map with the lat and long
    map_a = folium.Map(location=(final_df_pr.iloc[0]['latitude'],final_df_pr.iloc[0]['longitude']), zoom_start=12)

    # loop df, and add in palcemarks
    for row in final_df_pr.itertuples():
        pop_str = f"Neighborhood: {row.neighbourhood} <br> Host Name: {row.host_name} <br> Room Type: {row.room_type}"
        folium.Marker(
            location=(row.latitude,row.longitude),
            popup=folium.Popup(pop_str, min_width = 150, max_width = 200),
            tooltip = f"$ {row.price}"
        ).add_to(map_a)
else:
    map_a = folium.Map(location=(40.7580, -73.9855), zoom_start=12)

folium_static(map_a)
