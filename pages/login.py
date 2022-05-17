import streamlit as st
import pandas as pd
import utils.database as database
from hashlib import sha256

def create_page():
    # Handle when the user submits the form.
    def submit():
        email = st.session_state["login_email"]
        password = sha256((st.session_state["login_password"] + "1MPlGCnOwSywPTg5BXbZ").encode("utf-8")).hexdigest()
        del st.session_state["login_password"]
        
        # Create a database connection.
        conn = database.get_connection()
        
        # Check the email and password againsts the database.
        users = pd.read_sql("SELECT * FROM user", conn)
        for _, row in users.iterrows():
            if row["email"] == email and row["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.session_state["authentication_level"] = row["authentication_level"]
                
                st.success("Successfully logged in!")
                
                return
            
        st.error("The email or password is incorrect!")
    
    # Render the form.
    with st.form("login_form"):
        st.write("Login")
        
        st.text_input("Email", type="default", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        
        st.form_submit_button("Login", on_click=submit)