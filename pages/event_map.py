from branca.element import Template, MacroElement
from datetime import datetime
import pandas as pd
import streamlit as st
import utils.database as database
import streamlit.components.v1 as components
import folium

# pip install streamlit-folium

from utils.settings import read_settings 

def create_page():
    st.header("Event map")

    # Loads the longitude and latitude for positioning of the event map from the settings 
    settings = read_settings()
    latitude = settings["event_map"]["start_latitude"]
    longitude = settings["event_map"]["start_longitude"]
    
    # Expander to hide the filter options if the user does not want to use them
    with st.expander("Filter options"):

        # Create the select box to pick the sound type
        option_sound_type = st.selectbox("Select sound type", ["All", "Vehicle", "Gunshot", "Animal", "Unknown"])

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
        height="100%",
        width="100%",
    )
    
    folium.TileLayer('stamenterrain').add_to(m)
    
    ## Creates the legend
    with open("./components/legend.html") as f:
        legend = f.read()
    
    template = """
    {% macro html(this, kwargs) %}
    """ + legend + """
    {% endmacro %}
    """
    
    macro = MacroElement()
    macro._template = Template(template)

    m.add_child(macro)
    ##

    for _, event in df.iterrows():
        create_marker(event).add_to(m)

    # Auto zoom scaling based on nodes
    list_lat_lon = list(zip(df["latitude"], df["longitude"]))
    m.fit_bounds(list_lat_lon)

    # Creates a figure from the map,
    # then renders the html representation of the figure
    # then gives the html to streamlit to display
    fig = folium.Figure().add_child(m)
    components.html(fig.render(), height=700)
    
def get_color(event: pd.Series) -> str:
    import time as ti
    current_unix_time = ti.time()
    
    unix_5_min = 300 # 60sec * 5min
    unix_1_hr = 3600 # 60sec * 60min
    unix_6_hr = 21600
    unix_1_d = 86400
    unix_3_d = 259200

    if event["time"] >= current_unix_time - unix_5_min:
        return "red"
    elif event["time"] >= current_unix_time - unix_1_hr:
        return "orange"
    elif event["time"] >= current_unix_time - unix_6_hr:
        return "darkblue" 
    elif event["time"] >= current_unix_time - unix_1_d:
        return "blue"
    elif event["time"] >= current_unix_time - unix_3_d:
        return "lightblue"
    else:
        return "lightgray"
    
    
def create_marker(event: pd.Series) -> folium.Marker:
    color = get_color(event)
    if event["sound_type"] == "unknown":
        icon = folium.Icon(
            icon="question",
            prefix="fa fa-question",
            color=color
        )

    elif event["sound_type"] == "vehicle":
        icon  = folium.Icon(
            icon="car",
            prefix="fa fa-car",
            color=color
        )
        
    elif event["sound_type"] == "animal":
        icon= folium.Icon(
            icon="linux",
            prefix="fa fa-linux",
            color=color
        )
        
    elif event["sound_type"] == "gunshot":
        icon = folium.Icon(
            icon="exclamation",
            prefix="fa fa-exclamation",
            color=color 
        )
        
    return folium.Marker(
        location=[event["latitude"], event["longitude"]],
        popup=event["event_id"],
        icon=icon,
    )