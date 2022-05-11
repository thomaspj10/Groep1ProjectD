import json, streamlit as st


def create_page():
    # Reads the json file
    with open("../application_settings.json") as settings_file:
        settings = json.load(settings_file)

    st.title("Settings")

    with st.form("settings_form"):

        # Latitude and Longitude settings
        st.write("The coordinates for the starting location of the event map")
        settings["map"]["latitude"] = st.number_input("Latitude", value=settings["map"]["latitude"], format="%2.15f")
        settings["map"]["longitude"] = st.number_input("Longitude", value=settings["map"]["longitude"], format="%2.15f")

        # Creates a line
        st.markdown("---")
        
        # Refresh rate setting
        st.write("Explanation here...")
        settings["refresh_rate"] = st.number_input("Refresh rate in ms", value=settings["refresh_rate"])

        # Creates a line
        st.markdown("---")

        # SMS credentials setting
        st.write("Explanation here...")
        settings["sms_credentials"] = st.text_input("SMS credentials", value=settings["sms_credentials"])

        # Button to save settings
        submitted = st.form_submit_button("Save")

        if submitted:
            try: 
                with open("../application_settings.json", "w") as settings_file:
                    json.dump(settings, settings_file)
                    st.success("Settings have successfully changed.")
            except:
                st.error("Something went wrong, please try again.")
