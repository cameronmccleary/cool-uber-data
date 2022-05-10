'''
Name: Cameron McCleary
CS230: Section 5
Data: Uber Fares
URL:

Description: This app allows users to view data
from Uber in a number of formats including pie charts,
scatter plots and maps. Users may utilize sliders and
number selects to view information that most directly
suits their needs. I hope you enjoy!
'''

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import pydeck as pdk
import random as rd

df_uber = pd.read_csv("uber_8000_sample (2).csv")
df_uber = pd.DataFrame(df_uber)
def drop_data(column_name, amount):
    global df_uber
    df_uber = df_uber.drop(df_uber[df_uber[column_name] == amount].index)
    return df_uber
drop_data('passenger_count',0)
drop_data('pickup_longitude',0)
drop_data('pickup_latitude',0)
drop_data('dropoff_longitude',0)
drop_data('dropoff_latitude',0)

df_uber = df_uber.drop(df_uber[df_uber.fare_amount < 0].index)


st.title("Uber Fares Data")
st.subheader('Welcome to my app on Uber Data! Feel free to try anything out!')
st.image('Uber.webp', width=500)
df_uber.set_index('key', inplace=True)
# st.write(df_uber)
st.sidebar.header('Part I')
passengers = 1, 2, 3, 4, 5, 6

selected_chart = st.sidebar.selectbox('Please select a chart to show:', ['', 'Line Plot', 'Pie Chart'])


if selected_chart == "Line Plot":
    s1 = df_uber.loc[:, ['fare_amount', 'passenger_count']]
    average_fare = s1.groupby('passenger_count').mean()
    fig, ax = plt.subplots()
    ax.plot(passengers, average_fare['fare_amount'], color='r', marker='*')
    plt.xlabel('Passengers')
    plt.ylabel('Cost')
    plt.title('Cost vs. Passengers')
    st.pyplot(fig)

elif selected_chart == 'Pie Chart':
    s_df = df_uber.groupby(by=['passenger_count']).count()
    count = [5414, 1110, 354, 186, 572, 178]
    passen = [1,2,3,4,5,6]
    fig, ax = plt.subplots()
    ax.pie(count, labels=passen, autopct='%.1f%%')
    plt.title('Percentage of Passengers')
    st.pyplot(fig)

# PART II
st.sidebar.header('Part II')
fare = st.sidebar.slider('Please select a price to plot:', 0.0, 200.0)
if not fare:
    st.sidebar.write('Please select a price using the slider above.')
elif fare:
    s2 = df_uber[df_uber.fare_amount <= fare][['fare_amount']]
    time_fare = s2.groupby(s2.index).mean()
    fig, ax = plt.subplots()
    ax.scatter(time_fare.index, time_fare['fare_amount'], color='b', s=10)
    plt.xlabel('Time')
    plt.ylabel('Cost')
    plt.title('Time of Trip vs. Cost')
    plt.xticks([time_fare.index.min(), time_fare.index.max()])
    st.pyplot(fig)

# Part III
st.sidebar.header('Part III')
df_uber.rename(columns={"pickup_latitude": "lat", "pickup_longitude": "lon"}, inplace=True)
passenger_list = []

for c in df_uber.passenger_count:
    if c not in passenger_list:
        passenger_list.append(c)

#passenger_list = [passenger_list.append(c) for c in df_uber.passenger_count if c not in passenger_list]
#st.write(passenger_list)

sub_df_list = []

for c in passenger_list:
    sub_df = df_uber[df_uber["passenger_count"] == c]
    sub_df_list.append(sub_df)

layer_list = []

for sub_df in sub_df_list:
    layer = pdk.Layer(type='ScatterplotLayer',
                      data=sub_df,
                      get_position='[lon, lat]',
                      get_radius=100,
                      get_color=[255,0,0],
                      pickable=True
                      )
    layer_list.append(layer)

tool_tip = {"html": "<b>Price:</b> ${fare_amount} <br/> <b>Passengers:</b> {passenger_count}",
            "style": {"backgroundColor": "white",
                      "color": "red"}
            }

view_state = pdk.ViewState(
    latitude=df_uber["lat"].mean(),
    longitude=df_uber["lon"].mean(),
    zoom=11,
    pitch=0)

passenger_list.insert(0, "")

selected_passenger = st.sidebar.number_input("How many people are traveling today?", 0,6)

for i in range(len(passenger_list)):
    if selected_passenger == passenger_list[i]:
        if i == 0:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v10',
                initial_view_state=view_state,
                layers=layer_list,
                tooltip=tool_tip
            )
        else:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v10',
                initial_view_state=view_state,
                layers=[layer_list[i - 1]],
                tooltip=tool_tip
            )

        st.pydeck_chart(map)
