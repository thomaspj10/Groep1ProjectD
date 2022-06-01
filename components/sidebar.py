import streamlit as st

from pages import *
import utils.cookies as cookies

class AuthenticationLevel:
    NONE = 0
    RANGER = 1
    ADMINISTRATOR = 2

def create_page():
    available_pages = [
        Page("Login", AuthenticationLevel.NONE, pages.login.create_page),
        Page("Dashboard", AuthenticationLevel.RANGER, pages.dashboard.create_page),
        Page("Historical Data", AuthenticationLevel.RANGER, pages.historical_data.create_page),
        Page("Download Event", AuthenticationLevel.RANGER, pages.download_event.create_page),
        Page("Create Account", AuthenticationLevel.ADMINISTRATOR, pages.create_account.create_page),
        Page("Account Settings", AuthenticationLevel.RANGER, pages.acount_settings.create_page),
        Page("Application Settings", AuthenticationLevel.ADMINISTRATOR, pages.application_settings.create_page),
    ]

    # Get the authentication level of the current logged in user.
    current_authentication_level = 0
    if "authentication_level" in cookies.get_cookies():
        current_authentication_level = int(cookies.get_cookies()["authentication_level"])

        # make logout button in sidebar
        def logout_click():
            del cookies.get_cookies()["logged_in"]
            del cookies.get_cookies()["email"]
            del cookies.get_cookies()["authentication_level"]
            
        st.sidebar.button("Logout", on_click=logout_click)
        
        available_pages.remove(available_pages[0])
        #available_pages.remove(Page("Login", 0, pages.login.create_page))

    # Display the page options for the user based on their authentication level.
    choice = st.sidebar.radio("Choose your page: ",
        [page.name for page in available_pages if page.authentication_level <= current_authentication_level])

    # Render the currently active page.
    for page in available_pages:
        if page.name == choice:
            page.create_page()
            break

    
    # if account is logged in have a logout button
    #if "authentication_level" in st.session_state:
        
    #if pages.login.is_logged_in():
        #available_pages.append(Page("Logout", 0, pages.login.logout))
