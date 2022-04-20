import streamlit as st

from pages.page import Page
import pages.eventmap
import pages.login
import pages.register

def create_page():
    available_pages = [
        Page("Login", 0, pages.login.create_page),
        Page("Register", 2, pages.register.create_page),
        Page("Eventmap", 0, pages.eventmap.create_eventmap),
    ]
    
    # Get the authentication level of the current logged in user.
    current_authentication_level = 0
    if "authentication_level" in st.session_state:
        current_authentication_level = st.session_state["authentication_level"]
        
    # Display the page options for the user based on their authentication level.
    choice = st.sidebar.radio("Choose your page: ", 
        [page.name for page in available_pages if page.authentication_level <= current_authentication_level])

    # Render the currently active page.
    for page in available_pages:
        if page.name == choice:
            page.create_page()
            break