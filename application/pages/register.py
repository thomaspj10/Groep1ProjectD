import streamlit as st
import pandas as pd
from hashlib import sha256

def create_page():
    available_roles = [
        "Member",
        "Administrator"
    ]
    
    # Handle when the user submits the form.
    def submit():
        email = st.session_state["register_email"]
        telephone = st.session_state["register_telephone"]
        username = st.session_state["register_username"]
        password = sha256((st.session_state["register_password"] + "1MPlGCnOwSywPTg5BXbZ").encode("utf-8")).hexdigest()
        role = available_roles.index(st.session_state["register_role"]) + 1
        
        # TODO - Replace this with the api from https://github.com/thomaspj10/Groep1ProjectD/pull/2
        import sqlite3
        conn = sqlite3.connect("./application/db.sqlite")
        
        # Add the new user to the database.
        user_row = pd.DataFrame({
            "username": username,
            "password": password,
            "email": email,
            "telephone": telephone,
            "authentication_level": role
        }, index=[0])
        user_row.to_sql("user", conn, if_exists="append", index=False)
        
        st.success("Account created successfully!")
        
        del st.session_state["register_password"]
    
    # Render the form.
    with st.form("register_form", clear_on_submit=True):
        st.write("Register")
        
        st.text_input("Email", type="default", key="register_email")
        st.text_input("Phone Number", type="default", key="register_telephone")
        st.text_input("Username", type="default", key="register_username")
        st.text_input("Password", type="password", key="register_password")
        st.selectbox("Role", available_roles, key="register_role")
        
        st.form_submit_button("Create user", on_click=submit)