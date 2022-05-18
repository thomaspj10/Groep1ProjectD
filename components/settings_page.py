import streamlit as st
from utils.settings import read_settings, save_settings

def create_page():
    # Reads the json file
    settings = read_settings()

    st.title("Settings")

    with st.form("settings_form"):
        # Latitude and Longitude settings
        st.write("The coordinates for the starting location of the event map")
        settings["eventmap"]["latitude"] = st.number_input("Latitude", value=settings["eventmap"]["start_latitude"], format="%2.15f")
        settings["eventmap"]["longitude"] = st.number_input("Longitude", value=settings["eventmap"]["start_longitude"], format="%2.15f")

        # Creates a line
        st.markdown("---")
        
        # Refresh rate setting
        st.write("The refresh rate for refreshing the eventmap and recent events pages to show the updated data")
        settings["pages"]["refresh_rate_in_seconds"] = st.number_input("Refresh rate in seconds", value=settings["pages"]["refresh_rate_in_seconds"])

        # Creates a line
        st.markdown("---")

        # SMS credentials settings
        st.write("The credentials used for the SMS service")
        settings["twilio_sms_service"]["account_sid"] = st.text_input("Account SID", value=settings["twilio_sms_service"]["account_sid"])
        settings["twilio_sms_service"]["auth_token"] = st.text_input("Authentication token", value=settings["twilio_sms_service"]["auth_token"])
        settings["twilio_sms_service"]["messaging_service_sid"] = st.text_input("Messaging service SID", value=settings["twilio_sms_service"]["messaging_service_sid"])

        # Button to save settings
        submitted = st.form_submit_button("Save")

        if submitted:
            if save_settings(settings):
                st.success("Settings have successfully changed.")
            else:
                st.error("Something went wrong, please try again.")
