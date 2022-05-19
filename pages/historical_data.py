import streamlit as st
import datetime
import pandas as pd

def create_page():
    st.title("Historical Data")

    # Filtering/sorting options for Sound type, Probability, Node ID, Time and Date
    with st.expander("Filtering and sorting options"):
        with st.form("filter_form"):
            # Sound type filter
            st.markdown("##### Sound type")
            sound_type_input = st.selectbox("Sound type", ["All", "Car", "Animal", "Gunshot", "Unkown"])
            st.markdown("***")

            # Probability filter
            st.markdown("##### Probability")
            probability_input = st.slider(label="Minimal probability", value=0, min_value=0, max_value=100, step=1)
            st.markdown("***")

            # Node ID filter
            st.markdown("##### Node ID")
            node_id_input = st.number_input(label="Specific Node ID", min_value=-1, max_value=999, help="-1 = no filtering on Node ID")
            st.markdown("***")

            # Time filter
            st.markdown("##### Time")
            start_time_input = st.time_input(label="Starting time", value=datetime.time(0, 0, 0))
            end_time_input = st.time_input(label="Ending time", value=datetime.time(23, 59, 59))
            st.markdown("***")

            # Date filter
            st.markdown("##### Date")
            start_date_input = st.date_input(label="Starting date", value=pd.to_datetime(datetime.date.today() - pd.Timedelta(days=7)))
            end_date_input = st.date_input(label="Ending date", value=datetime.date.today())
            st.markdown("***")

            # Sorting options
            st.markdown("##### Sorting ")
            sorting_element_input = st.selectbox("Select the preferred type to sort", ["Date", "Probability", "Node ID", "Time"])
            sorting_order_input = st.selectbox("Select the sorting order", ["Descending", "Ascending"])
            st.markdown("***")

            submitted = st.form_submit_button("Apply filters/sorting")

            if submitted:
                st.write("Submitted")

            # Reset button
            # if st.button("Reset options"):
            #     sound_type_input = "All"
            #     probability_input = 0
            #     node_id_input = -1
            #     start_time_input = datetime.time(0, 0, 0)
            #     end_time_input = datetime.time(23, 59, 59)
            #     start_date_input = pd.to_datetime(datetime.date.today() - pd.Timedelta(days=7))
            #     end_date_input = datetime.date.today()
            #     sorting_element_input = "Date"
            #     sorting_order_input = "Descending"

    st.write(sorting_order_input)