from datetime import datetime
import pandas as pd
import streamlit as st
import utils.database as database
import streamlit.components.v1 as components
import folium

# pip install streamlit-folium

from utils.settings import read_settings 

def create_page():
    st.header("Folium")

    # Loads the longitude and latitude for positioning of the event map from the settings 
    settings = read_settings()
    latitude = settings["eventmap"]["start_latitude"]
    longitude = settings["eventmap"]["start_longitude"]
    
    # Expander to hide the filter options if the user does not want to use them
    with st.expander("Filter options"):

        # Create the select box to pick the sound type
        option_sound_type = st.selectbox("Select sound type", ["All", "Car", "Gun", "Animal", "Unknown"])

        # Create the slider to pick a value for probability (between 0 and 100 with steps of 1)
        probability_slider = st.slider(label = 'Probability', value = 0, min_value = 0, max_value = 100, step = 1)

        date_cols = st.columns(2)
        
        with date_cols[0]:
            # Create the date
            start = st.date_input('Start', value = datetime.today().date())

        with date_cols[1]:
            # add a year to start date
            end = st.date_input('End', value = pd.to_datetime(start + pd.Timedelta(days=365)))

        # convert date to unix timestamp
        start_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(start), '%Y-%m-%d')))
        end_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(end), '%Y-%m-%d')))
    
    # Create a database connection.
    conn = database.get_connection()

    df = pd.read_sql("SELECT * FROM event", conn)

    # Sound type filter
    if option_sound_type != "All":
        df = df[df["sound_type"] == option_sound_type.lower()] 

    # Filter probability
    df = df[df["probability"] >= probability_slider] 
    
    # Date filter
    df = df[(df["time"] >= start_to_unix_timestamp) & (df["time"] <= end_to_unix_timestamp)]
    
    # The map
    m = folium.Map(
        location=[latitude, longitude],
        # tiles="Stamen Terrain",
        height="100%",
        width="100%"
    )
    folium.TileLayer('stamenterrain').add_to(m)

    for _, event in df.iterrows():
        if event["sound_type"] == "unknown":
            icon = folium.Icon(
                icon="question",
                prefix="fa fa-question",
                color="gray"
            )

        elif event["sound_type"] == "vehicle":
            icon  = folium.Icon(
                icon="car",
                prefix="fa fa-car",
                color="blue"
            )
            
        elif event["sound_type"] == "animal":
            icon= folium.Icon(
                icon="car",
                prefix="fa fa-linux",
                # prefix="fa fa-exclamation"
                # prefix="fa fa-binoculars"
                color="green"
            )
            
        elif event["sound_type"] == "gunshot":
            icon = folium.Icon(
                icon="car",
                prefix="fa fa-exclamation",
                color="red"
            )
            
        folium.Marker(
            location=[event["latitude"], event["longitude"]],
            popup=event["event_id"],
            icon=icon,
        ).add_to(m)

    list_lat_lon = list(zip(df["latitude"], df["longitude"]))
    m.fit_bounds(list_lat_lon)

    # Creates a figure from the map,
    # then renders the html representation of the figure
    # then gives the html to streamlit to display
    fig = folium.Figure().add_child(m)
    components.html(fig.render(), height=700)