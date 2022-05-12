import json, streamlit as st
from utils.settings import read_settings, save_settings

def create_page():
    # Reads the json file
    settings = read_settings()

    st.title("Settings")

    with st.form("settings_form"):
        # Latitude and Longitude settings
        st.write("The coordinates for the starting location of the event map")
        settings["map"]["latitude"] = st.number_input("Latitude", value=settings["map"]["latitude"], format="%2.15f")
        settings["map"]["longitude"] = st.number_input("Longitude", value=settings["map"]["longitude"], format="%2.15f")

        # Creates a line
        st.markdown("---")
        
        # Refresh rate setting
        st.write("The refresh rate for refreshing the pages automatically")
        settings["refresh_rate"] = st.number_input("Refresh rate in ms", value=settings["refresh_rate"])

        # Creates a line
        st.markdown("---")

        # SMS credentials setting
        st.write("The credentials used for the SMS system")
        settings["sms_credentials"] = st.text_input("SMS credentials", value=settings["sms_credentials"])

        # Button to save settings
        submitted = st.form_submit_button("Save")

        if submitted:
            if save_settings(settings):
                st.success("Settings have successfully changed.")
            else:
                st.error("Something went wrong, please try again.")
