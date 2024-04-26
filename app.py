######################
# Import libraries
######################
"""In this project you are going to use Airbnb NYC 2019 housing data to build a streamlit app with following requirements:

1. [5pts] It greets users with a nice page with sufficient info describing the purpose of the webapp (you design your App name and logo etc.).

2.  [5pts] User will be able to see a few rows of the data as a table

3.  [10pts] User will be able to select one of the five NYC boroughs (Manhattan, Bronx, etc. ) from a drop down menu 
- The candidate boroughs in menu must come from the dataset instead of hard coding it (bot like selection=["Manhattan", "Bronx", ...])

4.  [20pts] User will then be able to select one or more of the neighborhoods (if Manhattan is selected then this multi-select drop down menu will have neighborhoods available in Mahanttan)

5.  [10pts] User should be able to set price range (on the main section instead of side menu)

6.  [10pts] After all the previous selections user should see something like:

  Total 15 housing rental are found in Midtown Manhattan with price between $500 and $800

The total entries can be 0

7.  [20pts] At this step a map shows with available apartment/house as markers; when clicking on it it shows details including "name", host name, room type, neighborhood, Price will be showing as tool tip.

e.g.,  Name: Furnished room in Astoria apartment
         Neighborhood: Astoria

         Host name: John

         Room type: Private room

Tooltip: $1000

8.  [10pts] Finally you should upload your app to streamlit site."""
import math
from datetime import datetime
import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image

######################
# Page Title
######################

# PIL.Image
# Create the header section
image = Image.open('download.png')
col0, col1, col2 = st.columns([0.3, 0.65, 3])  # Adjust the ratio based on your aesthetic preference

# col1.image(image, use_column_width=False)
col1.image(image, width = 80)
col2.title('NYC Airbnb Navigator')
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

# 7.  [20pts] At this step a map shows with available apartment/house as markers; when clicking on it it shows details including "name", host name, room type, neighborhood, Price will be showing as tool tip.

# e.g.,  Name: Furnished room in Astoria apartment
#          Neighborhood: Astoria

#          Host name: John

#          Room type: Private room
# map_df = final_df_pr.loc[0,["latitude", "longitude"]]
print(final_df_pr.iloc[0])
# # print(final_df_pr.loc[0,'longitude'])
map_a = folium.Map(location=(final_df_pr.iloc[0]['latitude'],final_df_pr.iloc[0]['longitude']), zoom_start=12)

count = 0
for row in final_df_pr.itertuples():
    pop_str = f"Neighborhood: {row.neighbourhood} <br> Host Name: {row.host_name} <br> Room Type: {row.room_type}"
    folium.Marker(
        location=(row.latitude,row.longitude),
        popup=folium.Popup(pop_str, min_width = 150, max_width = 200),
        tooltip = f"$ {row.price}"
    ).add_to(map_a)
    # count += 1
    # if count == 10:
    #     break

folium_static(map_a)

# st.header("Where are the most expensive properties located?")
# st.subheader("On a map")
# st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")

# # Get "latitude", "longitude", "price" for top listings
# toplistings = df.query("price>=800")[["name", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)


# Top = toplistings.values[0,:]
# m = folium.Map(location=Top[1:-1], zoom_start=16)

# tooltip = "Top listings"
# for j in range(50):
#     name, lat, lon, price = toplistings.values[j,:]
#     folium.Marker(
#             (lat,lon), popup=f"{name}" , tooltip=f"Price:{price}"
#         ).add_to(m)

# # call to render Folium map in Streamlit
# folium_static(m)


# st.write("---")

# st.markdown("""### Images and dropdowns

# Use [st.image](https://streamlit.io/docs/api.html#streamlit.image) to show images of cats, puppies, feature importance plots, tagged video frames, and so on.

# Now for a bit of fun.""")

# pics = {
#     "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
#     "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
#     "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg",
#     "Cheetah": "img/running-cheetah.jpeg",
#     "FT-Logo": "ft-logo.png"
# }
# pic = st.selectbox("Picture choices", list(pics.keys()), 0)
# st.image(pics[pic], use_column_width=True, caption=pics[pic])

# st.write("---")

# select_col = st.selectbox("Select Columns", list(df.columns), 0)
# st.write(f"Your selection is {select_col}")

