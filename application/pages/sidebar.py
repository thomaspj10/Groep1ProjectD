import streamlit as st

from pages.page import Page
import utils.cookies as cookies
import pages.eventmap
import pages.login
import pages.create_account
import pages.dashboard
import pages.recent_events

def create_page():
    available_pages = [
        Page("Login", 0, pages.login.create_page),
        Page("Create Account", 2, pages.create_account.create_page),
        Page("Dashboard", 1, pages.dashboard.create_page),
        Page("Eventmap", 1, pages.eventmap.create_eventmap),
        Page("Recent Events", 1, pages.recent_events.create_page)
    ]

    # Get the authentication level of the current logged in user.
    current_authentication_level = 0
    if "authentication_level" in cookies.get_cookies():
        current_authentication_level = cookies.get_cookies()["authentication_level"]

        # make logout button in sidebar
        def logout_click():
            del st.session_state["logged_in"]
            del st.session_state["email"]
            del st.session_state["authentication_level"]
        
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
