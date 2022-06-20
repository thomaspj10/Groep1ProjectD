import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import utils.database as database
import base64

def download_button(object_to_download, download_filename):
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link

def create_page():
    with st.form(key="dont_refresh", clear_on_submit=False):
        event_to_download = st.number_input("Enter event ID", value=1)
        submitted = st.form_submit_button("Download")
        
        if submitted:
            create_download(event_to_download)

def create_download(event_id = None):
    if event_id == None:
        event_id = st.experimental_get_query_params()["event"][0]
        if not event_id.isnumeric():
            return
    
    conn = database.get_connection()

    # Search for the specific event.
    df = pd.read_sql(f"SELECT * FROM event WHERE event_id={event_id} AND pdf IS NOT NULL", conn)
    
    if df.size == 0:
        st.write(f"A summary of the event {event_id} does not yet exist.")
        return

    pdf_bytes = df.iloc[0]["pdf"]
    
    components.html(
        download_button(pdf_bytes, f"Summary - event {event_id}.pdf"),
        height=0,
    )
    
    st.write("Download is finished.")