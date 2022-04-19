import streamlit as st
import pages.sidebar

def create_page():
    # Handle when the user submits the form.
    def submit():
        email = st.session_state["email"]
        password = st.session_state["password"]
        
        # TODO - Login check
        
        st.session_state["logged_in"] = True
        st.session_state["authentication_level"] = 1
        
        del st.session_state["password"]
    
    # Render the form.
    with st.form("login_form"):
        st.write("Login")
        
        st.text_input("Email", type="default", key="email")
        st.text_input("Password", type="password", key="password")
        
        st.form_submit_button("Login", on_click=submit)