import streamlit as st
import pandas as pd
import utils.database as database

def create_page():
    with st.form(key="dont_refresh", clear_on_submit=False):
        event_to_download = st.number_input("Enter event ID", value=1)
        submitted = st.form_submit_button("Create download link")
        
        if submitted:
            import streamlit.components.v1 as components
            components.iframe(f"http://localhost:8501?event={event_to_download}", width=500, height=500, scrolling=False)


def create_download():
    event_id = st.experimental_get_query_params()["event"][0]
    if not event_id.isnumeric():
        return
    
    conn = database.get_connection()
    
    # Search for the specific event.
    df = pd.read_sql(f"SELECT * FROM event WHERE event_id={event_id} AND pdf IS NOT NULL", conn)
    
    if df.size == 0:
        st.write(f"An summary of the event {event_id} does not yet exist.")
        return

    def on_download():
        st.experimental_set_query_params(
            event=None
        )

    st.write("Download is ready:")
    
    pdf_bytes = df.iloc[0]["pdf"]
    
    # Create the download button.
    st.download_button(
        label="Download the summary", 
        data=pdf_bytes, 
        file_name="summary.pdf", 
        on_click=on_download,
        key="dont_refresh"
    )