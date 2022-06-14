from math import ceil
from re import L
from turtle import onclick
from requests import session
import streamlit as st
import datetime
from time import mktime
import pandas as pd
from utils.database import get_connection


def create_page():
    if 'page' not in st.session_state:
        st.session_state.page = 0
    
    st.title("Historical Data")

    # Filtering/sorting options for Sound type, Probability, Node ID and Date
    with st.expander("Filtering and sorting options"):
        with st.form("filter_form"):
            cols = st.columns(2)
            with cols[0]:
                # Sound type filter
                st.markdown("##### Sound type")
                sound_type_input = st.selectbox("Sound type", ["All", "Vehicle", "Animal", "Gunshot", "Unknown"])
                st.markdown("***")

                # Date filter
                st.markdown("##### Date")
                start_date_input = st.date_input(label="Starting date", value=pd.to_datetime(datetime.datetime.now() - datetime.timedelta(days=7)))
                end_date_input = st.date_input(label="Ending date", value=datetime.datetime.now())
                st.markdown("***")

            with cols[1]:
                # Node ID filter
                st.markdown("##### Node ID")
                node_id_input = st.number_input(label="Specific Node ID", min_value=-1, max_value=999, help="-1 = no filtering on Node ID")
                st.markdown("***")

                # Sorting options
                st.markdown("##### Sorting ")
                sorting_element_input = st.selectbox("Select the preferred type to sort", ["Date", "Probability", "Node ID"])
                sorting_order_input = st.selectbox("Select the sorting order", ["Descending", "Ascending"])
                st.markdown("***")

            # Probability filter
            st.markdown("##### Probability")
            probability_input = st.slider(label="Minimal probability", value=0, min_value=0, max_value=100, step=1)
            st.markdown("***")

            submitted = st.form_submit_button("Apply filters/sorting")

            if submitted:
                st.session_state.page = 0
                st.success("Filters and sorting applied.")
    
    # Gets database connection
    conn = get_connection()

    # Gets all the records
    df = pd.read_sql("SELECT * FROM event", conn)

    # All the filtering options
    if (sound_type_input != "All"):
        df = df[df['sound_type'] == sound_type_input.lower()]

    df = df[(df["time"] >= mktime(start_date_input.timetuple())) & (df["time"] <= mktime((end_date_input + datetime.timedelta(days = 1)).timetuple()))]

    if (node_id_input != -1):
        df = df[df['node_id'] == node_id_input]

    df = df[df['probability'] >= probability_input]

    # Sets the maximum page
    max_page = ceil(df.shape[0] / 10) - 1

    # Sorts with the values and order and only shows 'limit' rows with the page offset 
    limit = 10
    offset = st.session_state.page * 10
    df = df.sort_values(sorting_element_input.replace(" ", "_").replace("Date", "time").lower(), ascending="Ascending" == sorting_order_input).iloc[offset : offset + limit]

    # Adds a date column
    df['date'] = df['time']

    # Reorders the columns such that 'date' will now come after Node ID, instead of at the end 
    df = df.reindex(columns=['event_id', 'node_id', 'date', 'time', 'latitude', 'longitude', 'sound_type', 'probability', 'sound'])

    # Sets the types of the columns so the data can be changed to make it more readable
    df = df.astype({'date': str, 'time': str, 'probability': str})

    # Changes the date, time and probability values to make it more readable
    for index, event, in df.iterrows():
        df.at[index, 'time'] = datetime.datetime.fromtimestamp(int(event['time'])).strftime("%H:%M:%S")
        df.at[index, 'date'] = datetime.datetime.fromtimestamp(int(event['date'])).strftime("%d-%m-%Y")
        df.at[index, 'probability'] += '%'

    # Creates one row of columns with the names
    cols = st.columns(9)
    cols[0].subheader('Event ID')
    cols[1].subheader('Node ID')
    cols[2].subheader('Date')
    cols[3].subheader('Time')
    cols[4].subheader('Latitude')
    cols[5].subheader('Longitude')
    cols[6].subheader('Sound type')
    cols[7].subheader('Probability')
    cols[8].subheader('Sound')

    # For each row in the dataframe a row will be added with the values
    for index, event in df.iterrows():
        cols = st.columns(9)
        cols[0].text(df.at[index, 'event_id'])
        cols[1].text(df.at[index, 'node_id'])
        cols[2].text(df.at[index, 'date'])
        cols[3].text(df.at[index, 'time'])
        cols[4].text(df.at[index, 'latitude'])
        cols[5].text(df.at[index, 'longitude'])
        cols[6].text(df.at[index, 'sound_type'])
        cols[7].text(df.at[index, 'probability'])
        cols[8].audio(df.at[index, 'sound'])
    
    btn_cols = st.columns(5)
    with btn_cols[1]:
        st.button("< Previous page", disabled=st.session_state.page == 0, on_click=previous_page)
    with btn_cols[2]:
        st.markdown(f"#### Current page: {st.session_state.page + 1}")
    with btn_cols[3]:
        st.button("Next page > ", disabled=st.session_state.page >= max_page, on_click=next_page)

def previous_page():
    st.session_state.page -= 1

def next_page():    
    st.session_state.page += 1