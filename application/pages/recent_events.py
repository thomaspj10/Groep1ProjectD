import streamlit as st
import utils.database as database
import pandas as pd

def create_page():
    connection = database.get_connection()
    
    # Reads the events and orders by time (most recent first)
    events = pd.read_sql("SELECT * FROM event ORDER BY time DESC LIMIT 10", connection)

    # Shows the table with the events
    st.dataframe(events)